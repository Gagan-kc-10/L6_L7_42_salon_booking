
import math


def parse_booking(text):
    if not isinstance(text, str):
        raise ValueError("Booking must be provided as text.")

    if text.count(':') != 1:
        raise ValueError("Enter booking in service:duration format.")

    service, minutes = text.split(':')
    service = service.strip()

    if not service:
        raise ValueError("Service name cannot be empty.")

    try:
        duration = float(minutes.strip())
    except ValueError:
        raise ValueError("Duration must be a valid number.")

    if not math.isfinite(duration) or duration < 0:
        raise ValueError("Duration must be a finite, non-negative number.")

    return service.title(), duration


def duration_average(durations_csv):
    if not isinstance(durations_csv, str) or not durations_csv.strip():
        raise ValueError("Durations must be provided as CSV text.")

    try:
        values = [int(value.strip()) for value in durations_csv.split(',')]
    except ValueError:
        raise ValueError("All durations must be valid integers.")

    if not values or any(value < 0 for value in values):
        raise ValueError("Durations must be non-negative integers.")

    return sum(values) // len(values)


def payable_bill(text):
    if not isinstance(text, str) or text.count('|') != 1:
        raise ValueError("Enter bill in bill|discount format.")

    bill, discount = text.split('|')

    try:
        bill = float(bill.strip())
        discount = float(discount.strip())
    except ValueError:
        raise ValueError("Bill and discount must be valid numbers.")

    if not math.isfinite(bill) or not math.isfinite(discount):
        raise ValueError("Bill and discount must be finite numbers.")

    if bill < 0 or discount < 0:
        raise ValueError("Bill and discount cannot be negative.")

    total = bill * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)


if __name__ == "__main__":
    main()
