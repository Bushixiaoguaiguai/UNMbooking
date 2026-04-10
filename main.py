from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tkcalendar import DateEntry


URL = "https://apps.nottingham.edu.my/jw/web/userview/sport_booking/sport_complex_homepage/_/sport_complex"
SPORT_TYPE = "Badminton"
FACILITY_OPTIONS = ["Badminton Court 1", "Badminton Court 2"]
CHECK_IN_TIME_OPTIONS = [f"{hour:02d}:01" for hour in range(7, 22)]
CHECK_OUT_TIME_OPTIONS = [f"{hour:02d}:00" for hour in range(8, 23)]


@dataclass
class Account:
    key: str
    label: str
    username: str
    password: str
    contact_no: str
    full_name: str


@dataclass
class BookingConfig:
    account: Account
    facility_name: str
    check_in_dt: datetime
    check_out_dt: datetime
    purpose: str
    auto_submit_complete: bool


def load_accounts_from_env() -> dict[str, Account]:
    load_dotenv()

    raw_ids = os.getenv("ACCOUNT_IDS", "").strip()
    if not raw_ids:
        raise ValueError("Missing ACCOUNT_IDS in .env")

    account_ids = [x.strip() for x in raw_ids.split(",") if x.strip()]
    accounts: dict[str, Account] = {}

    for acc_id in account_ids:
        prefix = acc_id.upper()

        label = os.getenv(f"{prefix}_LABEL", acc_id)
        username = os.getenv(f"{prefix}_USERNAME", "").strip()
        password = os.getenv(f"{prefix}_PASSWORD", "").strip()
        contact_no = os.getenv(f"{prefix}_CONTACT_NO", "").strip()
        full_name = os.getenv(f"{prefix}_FULL_NAME", "").strip()

        if not username or not password:
            raise ValueError(f"Missing username/password for account prefix: {prefix}")

        accounts[acc_id] = Account(
            key=acc_id,
            label=label,
            username=username,
            password=password,
            contact_no=contact_no,
            full_name=full_name,
        )

    return accounts


def parse_datetime_text(text: str) -> datetime:
    """
    Accepts format: YYYY-MM-DD HH:MM
    Example: 2026-04-13 10:00
    """
    return datetime.strptime(text.strip(), "%Y-%m-%d %H:%M")


def datetime_to_picker_parts(dt: datetime) -> tuple[str, str, str, str]:
    """
    Converts datetime into:
    month label, year string, day string, time string
    Example: Apr, 2026, 13, 10:00
    """
    return dt.strftime("%b"), dt.strftime("%Y"), str(dt.day), dt.strftime("%H:%M")


def build_gui(accounts: dict[str, Account]) -> BookingConfig:
    root = tk.Tk()
    root.title("UNM Sport Booking")
    root.geometry("520x420")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=16)
    main_frame.pack(fill="both", expand=True)

    account_values = [f"{acc.key} | {acc.label}" for acc in accounts.values()]
    default_account = account_values[0]
    today_text = datetime.today().strftime("%Y-%m-%d")

    account_var = tk.StringVar(value=default_account)
    facility_var = tk.StringVar(value=FACILITY_OPTIONS[0])
    check_in_date_var = tk.StringVar(value=today_text)
    check_in_time_var = tk.StringVar(value="18:01")
    check_out_date_var = tk.StringVar(value=today_text)
    check_out_time_var = tk.StringVar(value="20:00")
    purpose_var = tk.StringVar(value="play badminton with friends")
    auto_submit_var = tk.BooleanVar(value=False)

    row = 0

    ttk.Label(main_frame, text="Account").grid(row=row, column=0, sticky="w", pady=6)
    account_combo = ttk.Combobox(
        main_frame,
        textvariable=account_var,
        values=account_values,
        state="readonly",
        width=40,
    )
    account_combo.grid(row=row, column=1, sticky="ew", pady=6)
    row += 1

    ttk.Label(main_frame, text="Facility").grid(row=row, column=0, sticky="w", pady=6)
    facility_combo = ttk.Combobox(
        main_frame,
        textvariable=facility_var,
        values=FACILITY_OPTIONS,
        state="readonly",
        width=40,
    )
    facility_combo.grid(row=row, column=1, sticky="ew", pady=6)
    row += 1

    ttk.Label(main_frame, text="Check-in").grid(row=row, column=0, sticky="w", pady=6)
    check_in_frame = ttk.Frame(main_frame)
    check_in_frame.grid(row=row, column=1, sticky="ew", pady=6)
    DateEntry(
        check_in_frame,
        textvariable=check_in_date_var,
        date_pattern="yyyy-mm-dd",
        width=24,
    ).pack(side="left", fill="x", expand=True)
    ttk.Combobox(
        check_in_frame,
        textvariable=check_in_time_var,
        values=CHECK_IN_TIME_OPTIONS,
        state="readonly",
        width=12,
    ).pack(side="left", padx=(8, 0))
    row += 1

    ttk.Label(main_frame, text="Check-out").grid(row=row, column=0, sticky="w", pady=6)
    check_out_frame = ttk.Frame(main_frame)
    check_out_frame.grid(row=row, column=1, sticky="ew", pady=6)
    DateEntry(
        check_out_frame,
        textvariable=check_out_date_var,
        date_pattern="yyyy-mm-dd",
        width=24,
    ).pack(side="left", fill="x", expand=True)
    ttk.Combobox(
        check_out_frame,
        textvariable=check_out_time_var,
        values=CHECK_OUT_TIME_OPTIONS,
        state="readonly",
        width=12,
    ).pack(side="left", padx=(8, 0))
    row += 1

    ttk.Label(main_frame, text="Purpose").grid(row=row, column=0, sticky="w", pady=6)
    ttk.Entry(main_frame, textvariable=purpose_var, width=42).grid(row=row, column=1, sticky="ew", pady=6)
    row += 1

    ttk.Label(main_frame, text="Date format").grid(row=row, column=0, sticky="w", pady=6)
    ttk.Label(main_frame, text="YYYY-MM-DD").grid(row=row, column=1, sticky="w", pady=6)
    row += 1

    ttk.Checkbutton(
        main_frame,
        text="Auto click Complete",
        variable=auto_submit_var,
    ).grid(row=row, column=1, sticky="w", pady=10)
    row += 1

    result: dict[str, BookingConfig] = {}

    def on_submit() -> None:
        try:
            selected_account_key = account_var.get().split("|")[0].strip()
            account = accounts[selected_account_key]

            check_in_dt = parse_datetime_text(f"{check_in_date_var.get()} {check_in_time_var.get()}")
            check_out_dt = parse_datetime_text(f"{check_out_date_var.get()} {check_out_time_var.get()}")

            if check_out_dt <= check_in_dt:
                raise ValueError("Check-out must be later than Check-in.")

            purpose_text = purpose_var.get().strip()
            if not purpose_text:
                raise ValueError("Purpose cannot be empty.")

            result["config"] = BookingConfig(
                account=account,
                facility_name=facility_var.get().strip(),
                check_in_dt=check_in_dt,
                check_out_dt=check_out_dt,
                purpose=purpose_text,
                auto_submit_complete=auto_submit_var.get(),
            )
            root.destroy()

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    ttk.Button(main_frame, text="Start Booking", command=on_submit).grid(
        row=row, column=1, sticky="e", pady=12
    )

    main_frame.columnconfigure(1, weight=1)
    root.mainloop()

    if "config" not in result:
        raise RuntimeError("Booking cancelled by user.")

    return result["config"]


def login_if_needed(page, account: Account) -> None:
    print(f"Current URL before login check: {page.url}")

    if "/jw/web/login" in page.url:
        print("Login page detected. Filling in credentials...")

        page.get_by_role("textbox", name="Username").fill(account.username)
        page.get_by_role("textbox", name="Password").fill(account.password)
        page.get_by_role("button", name="Login").click()

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        print(f"Current URL after login: {page.url}")
    else:
        print("Login not required.")


def open_new_booking_page(page, context):
    print("Waiting for sport complex homepage to be ready...")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    print("Clicking 'Other Facilities Online' and waiting for new tab...")
    with context.expect_page() as new_page_info:
        page.get_by_role("link", name="Other Facilities Online").click()

    booking_page = new_page_info.value
    booking_page.wait_for_load_state("domcontentloaded")
    booking_page.wait_for_timeout(2000)

    print(f"New tab opened: {booking_page.url}")

    print("Clicking 'Booking Request'...")
    booking_page.get_by_role("link", name="  Booking Request ").click()
    booking_page.wait_for_timeout(1500)

    print("Clicking 'New Booking'...")
    booking_page.get_by_role("link", name="New Booking").click()
    booking_page.wait_for_load_state("domcontentloaded")
    booking_page.wait_for_timeout(2000)

    print(f"Arrived at: {booking_page.url}")
    return booking_page


def pick_datetime(page, field_name: str, dt: datetime) -> None:
    month, year, day, time_text = datetime_to_picker_parts(dt)

    print(f"Opening date picker for: {field_name}")
    field = page.get_by_role("textbox", name=field_name)
    field.click()
    page.wait_for_timeout(1000)

    datepicker = page.locator("#ui-datepicker-div")
    datepicker.wait_for(state="visible", timeout=10000)

    print(f"Selecting month={month}, year={year}, day={day}, time={time_text}")

    datepicker.get_by_label("Select month").select_option(label=month)
    page.wait_for_timeout(300)

    datepicker.get_by_label("Select year").select_option(label=year)
    page.wait_for_timeout(300)

    datepicker.get_by_role("link", name=day, exact=True).click()
    page.wait_for_timeout(500)

    time_box = datepicker.get_by_role("textbox")
    time_box.click()
    time_box.fill(time_text)
    page.wait_for_timeout(500)

    time_box.press("Enter")
    page.wait_for_timeout(800)

    print(f"{field_name} selected.")


def fill_booking_time(page, cfg: BookingConfig) -> None:
    print("Picking check-in and check-out with the date picker...")

    pick_datetime(page=page, field_name="Check-in", dt=cfg.check_in_dt)
    pick_datetime(page=page, field_name="Check-out", dt=cfg.check_out_dt)

    page.wait_for_timeout(1000)

    print("Clicking 'Proceed'...")
    page.get_by_role("button", name="Proceed").click()

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)

    print(f"After Proceed URL: {page.url}")


def fill_basic_info(page, cfg: BookingConfig) -> None:
    print("Filling applicant information...")

    account = cfg.account
    email_value = f"{account.username}@nottingham.edu.my"

    page.get_by_role("textbox", name="Email *").fill(email_value)
    page.get_by_role("textbox", name="Contact No. *").fill(account.contact_no)
    page.get_by_role("textbox", name="Purpose *").fill(cfg.purpose)

    page.wait_for_timeout(1000)


def get_form_grid_frame(page):
    print("Locating form grid iframe...")

    frame_locator = page.frame_locator(
        'iframe[name="formGridFrame_formgrid_field13__164309675394793675031_861253476"]'
    )

    frame_locator.get_by_role("button", name="Select Facility").wait_for(timeout=10000)
    return frame_locator


def add_row(page) -> None:
    print("Clicking 'Add Rows'...")
    page.locator("#formgrid_field13__164309675394793675031_861253476").get_by_title("Add Rows").click()
    page.wait_for_timeout(1500)


def select_facility(page, cfg: BookingConfig) -> None:
    print("Opening facility selector inside iframe...")

    form_frame = get_form_grid_frame(page)
    form_frame.get_by_role("button", name="Select Facility").click()
    page.wait_for_timeout(2000)

    print(f"Selecting facility: {cfg.facility_name}")

    popup_frame = form_frame.frame_locator(
        'iframe[name="popupSelectFrame_popupselect__100698416494793674811_472784952"]'
    )

    popup_frame.get_by_role(
        "row",
        name=f" {cfg.facility_name} Badminton Court"
    ).locator("i").click()

    page.wait_for_timeout(1000)

    print("Confirming selected facility...")
    popup_frame.get_by_role("button", name="Select Facility").click()
    page.wait_for_timeout(2000)


def select_sport_type(page) -> None:
    print(f"Selecting sport type: {SPORT_TYPE}")

    form_frame = get_form_grid_frame(page)
    sport_field = form_frame.get_by_label("Type of Sports *")
    sport_field.click()
    sport_field.select_option(label=SPORT_TYPE)

    page.wait_for_timeout(1500)


def submit_selected_row(page) -> None:
    print("Submitting the selected facility row...")

    form_frame = get_form_grid_frame(page)
    submit_button = form_frame.get_by_role("button", name="Submit")
    submit_button.wait_for(timeout=10000)
    submit_button.click()

    page.wait_for_timeout(2500)
    print("Facility row submitted.")


def tick_confirmation(page) -> None:
    print("Ticking final confirmation checkbox/icon...")
    page.locator("label > i").click()
    page.wait_for_timeout(1500)


def pause_before_complete(page) -> None:
    print("Waiting for the Complete button...")
    complete_button = page.get_by_role("button", name="Complete")
    complete_button.wait_for(timeout=10000)

    print("Complete button is ready. Pausing before final click.")
    page.pause()


def complete_booking(page) -> None:
    print("Waiting for the Complete button...")
    complete_button = page.get_by_role("button", name="Complete")
    complete_button.wait_for(timeout=10000)

    print("Clicking Complete button...")
    complete_button.click()

    page.wait_for_timeout(3000)
    print("Booking submitted.")


def run_booking(cfg: BookingConfig) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("Opening the sport complex booking page...")
            page.goto(URL, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            login_if_needed(page, cfg.account)

            print("Ensuring we are back on the sport complex homepage...")
            page.wait_for_timeout(2000)
            print(f"Current page URL: {page.url}")

            booking_page = open_new_booking_page(page, context)

            fill_booking_time(booking_page, cfg)
            fill_basic_info(booking_page, cfg)
            add_row(booking_page)
            select_facility(booking_page, cfg)
            select_sport_type(booking_page)
            submit_selected_row(booking_page)
            tick_confirmation(booking_page)

            if cfg.auto_submit_complete:
                complete_booking(booking_page)
                print("Waiting 5 seconds before closing browser...")
                booking_page.wait_for_timeout(5000)
            else:
                pause_before_complete(booking_page)

        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}")
            page.pause()
        except Exception as e:
            print(f"Unexpected error: {e}")
            page.pause()
        finally:
            browser.close()


def main() -> None:
    accounts = load_accounts_from_env()
    cfg = build_gui(accounts)
    run_booking(cfg)


if __name__ == "__main__":
    main()
