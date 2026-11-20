import argparse
from scripts import generate_iphone, generate_ipad, generate_mac, generate_ios_promo


def main():
    parser = argparse.ArgumentParser(description="Generate Power Planner App Store screenshots and promo assets.")
    parser.add_argument(
        "--target",
        choices=["all", "iphone", "ipad", "mac", "promo"],
        default="all",
        help="Which asset set to generate (default: all)",
    )
    args = parser.parse_args()

    if args.target in ("all", "iphone"):
        generate_iphone.run()
    if args.target in ("all", "ipad"):
        generate_ipad.run()
    if args.target in ("all", "mac"):
        generate_mac.run()
    if args.target in ("all", "promo"):
        generate_ios_promo.run()


if __name__ == "__main__":
    main()
