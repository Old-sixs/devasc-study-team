from datetime import datetime


DEVICES = [
    {
        "hostname": "core-sw-01",
        "type": "Switch",
        "ip": "192.168.1.1",
        "location": "DataCenter-A",
        "status": "Active",
        "cpu_usage": 45,  
        "memory_usage": 62,  
        "uptime_days": 120,
        "backup_status": "Success",
    },
    {
        "hostname": "core-rt-01",
        "type": "Router",
        "ip": "192.168.1.254",
        "location": "DataCenter-A",
        "status": "Active",
        "cpu_usage": 88,  
        "memory_usage": 70,
        "uptime_days": 45,
        "backup_status": "Success",
    },
    {
        "hostname": "edge-fw-01",
        "type": "Firewall",
        "ip": "10.0.0.1",
        "location": "HQ-Building",
        "status": "Active",
        "cpu_usage": 30,
        "memory_usage": 92,  
        "uptime_days": 210,
        "backup_status": "Success",
    },
    {
        "hostname": "access-sw-01",
        "type": "Switch",
        "ip": "10.0.10.11",
        "location": "HQ-Building",
        "status": "Active",
        "cpu_usage": 15,
        "memory_usage": 40,
        "uptime_days": 5,  
        "backup_status": "Failed",  
    },
    {
        "hostname": "access-sw-02",
        "type": "Switch",
        "ip": "10.0.10.12",
        "location": "HQ-Building",
        "status": "Down",  
        "cpu_usage": 0,
        "memory_usage": 0,
        "uptime_days": 0,
        "backup_status": "Failed",
    },
    {
        "hostname": "branch-rt-01",
        "type": "Router",
        "ip": "172.16.1.1",
        "location": "Branch-East",
        "status": "Active",
        "cpu_usage": 95,  
        "memory_usage": 89,  
        "uptime_days": 300,
        "backup_status": "Success",
    },
    {
        "hostname": "branch-sw-01",
        "type": "Switch",
        "ip": "172.16.1.10",
        "location": "Branch-East",
        "status": "Active",
        "cpu_usage": 22,
        "memory_usage": 35,
        "uptime_days": 180,
        "backup_status": "Success",
    },
    {
        "hostname": "edge-fw-02",
        "type": "Firewall",
        "ip": "10.0.0.2",
        "location": "DataCenter-A",
        "status": "Maintenance",  
        "cpu_usage": 5,
        "memory_usage": 15,
        "uptime_days": 12,
        "backup_status": "Pending",
    },
]


CPU_THRESHOLD = 90  
MEM_THRESHOLD = 95  
UPTIME_THRESHOLD = 7  



def evaluate_device_health(device):
    """Evaluates a single device dictionary against operational rules

    and returns a list of active alerts/flags.
    """
    flags = []

   
    if device["status"] != "Active":
        flags.append(f"Status is {device['status']}")

    if device["cpu_usage"] > CPU_THRESHOLD:
        flags.append(f"High CPU ({device['cpu_usage']}%)")

    if device["memory_usage"] > MEM_THRESHOLD:
        flags.append(f"High Memory ({device['memory_usage']}%)")

    if device["uptime_days"] < UPTIME_THRESHOLD and device["status"] == "Active":
        flags.append(f"Low Uptime ({device['uptime_days']} days)")

    if device["backup_status"] != "Success":
        flags.append(f"Backup {device['backup_status']}")

    return flags


def generate_report():
    print("=" * 80)
    print("                  NETWORK OPERATIONAL STATUS REPORT                  ")
    print(f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    type_counts = {}
    location_counts = {}
    attention_list = []

    header_format = (
        "{:<13} {:<10} {:<15} {:<14} {:<8} {:<8} {:<8} {:<8}"
    )
    print(
        header_format.format(
            "Hostname",
            "Type",
            "IP Address",
            "Location",
            "Status",
            "CPU",
            "Mem",
            "Uptime",
        )
    )
    print("-" * 80)

    for dev in DEVICES:
        print(
            header_format.format(
                dev["hostname"],
                dev["type"],
                dev["ip"],
                dev["location"],
                dev["status"],
                f"{dev['cpu_usage']}%",
                f"{dev['memory_usage']}%",
                f"{dev['uptime_days']}d",
            )
        )

        dev_type = dev["type"]
        type_counts[dev_type] = type_counts.get(dev_type, 0) + 1

        loc = dev["location"]
        location_counts[loc] = location_counts.get(loc, 0) + 1

        alerts = evaluate_device_health(dev)
        if alerts:
            attention_list.append((dev["hostname"], dev["ip"], alerts))

    print("=" * 80)
    print("\n--- SUMMARY TOTALS ---")
    print("\nDevices by Type:")
    for d_type, count in type_counts.items():
        print(f"  • {d_type:<10}: {count}")

    print("\nDevices by Location:")
    for loc, count in location_counts.items():
        print(f"  • {loc:<14}: {count}")

    print("\n" + "=" * 80)
    print("ALERT!  DEVICES REQUIRING ATTENTION")
    print("=" * 80)

    if attention_list:
        for hostname, ip, issues in attention_list:
            issue_str = ", ".join(issues)
            print(f"• {hostname:<13} ({ip:<14}) ---> FLAGS: {issue_str}")
    else:
        print("All systems operating within normal parameters.")

    print("=" * 80)


if __name__ == "__main__":
    generate_report()