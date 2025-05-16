import argparse

DATA_COLLECTION_MODE = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telemetry system main entry point.")
    parser.add_argument(
        "mode",
        choices=["datacollection", "passthroughmode"],
        help="Mode to run the program in. Choose 'datacollection' or 'passthroughmode'."
    )

    args = parser.parse_args()
    mode = args.mode

    print(f"Running in {mode} mode...\n")

    if mode == "datacollection":
        DATA_COLLECTION_MODE = True
    
    # continue here
