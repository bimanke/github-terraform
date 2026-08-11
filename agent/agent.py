import json


# ==========================================================
# CRITICAL AZURE RESOURCES
# ==========================================================

CRITICAL_RESOURCES = {
    "azurerm_key_vault",
    "azurerm_storage_account",
    "azurerm_network_security_group",
    "azurerm_firewall",
    "azurerm_virtual_network",
    "azurerm_subnet",
    "azurerm_kubernetes_cluster",
    "azurerm_sql_server",
}


# ==========================================================
# POLICY CONFIGURATION
# ==========================================================

MAX_TOTAL_CHANGES = 20
MAX_PRODUCTION_CHANGES = 10


# ==========================================================
# MAIN POLICY ENGINE
# ==========================================================

def evaluate_policy(plan):

    resource_changes = plan.get("resource_changes", [])

    create_count = 0
    update_count = 0
    delete_count = 0

    critical_changes = []

    # ======================================================
    # ANALYZE EACH RESOURCE
    # ======================================================

    for resource in resource_changes:

        resource_type = resource.get("type", "")
        resource_name = resource.get("name", "")

        change = resource.get("change", {})
        actions = change.get("actions", [])

        # --------------------------------------------------
        # CREATE
        # --------------------------------------------------

        if "create" in actions:
            create_count += 1

        # --------------------------------------------------
        # UPDATE
        # --------------------------------------------------

        if "update" in actions:
            update_count += 1

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        if "delete" in actions:
            delete_count += 1

        # --------------------------------------------------
        # CRITICAL RESOURCE
        # --------------------------------------------------

        if resource_type in CRITICAL_RESOURCES:

            if any(
                action in actions
                for action in ["create", "update", "delete"]
            ):

                critical_changes.append(
                    f"{resource_type}.{resource_name}"
                )

    total_changes = (
        create_count +
        update_count +
        delete_count
    )

    # ======================================================
    # DISPLAY PLAN SUMMARY
    # ======================================================

    print("------------------------------------")
    print("Terraform Plan Analysis")
    print("------------------------------------")

    print(f"Create           : {create_count}")
    print(f"Update           : {update_count}")
    print(f"Delete           : {delete_count}")
    print(f"Total Changes    : {total_changes}")
    print(
        f"Critical Changes : "
        f"{len(critical_changes)}"
    )

    if critical_changes:

        print("\nCritical Resources:")

        for resource in critical_changes:
            print(f"  - {resource}")

    # ======================================================
    # RULE 1
    # ANY DELETE = REJECT
    # ======================================================

    if delete_count > 0:

        return (
            "REJECT",
            (
                f"Terraform plan contains "
                f"{delete_count} resource deletion(s). "
                f"Automatic deployment is not allowed."
            )
        )

    # ======================================================
    # RULE 2
    # TOO MANY CHANGES = REJECT
    # ======================================================

    if total_changes > MAX_TOTAL_CHANGES:

        return (
            "REJECT",
            (
                f"Terraform plan contains "
                f"{total_changes} changes. "
                f"Maximum allowed is "
                f"{MAX_TOTAL_CHANGES}."
            )
        )

    # ======================================================
    # RULE 3
    # PRODUCTION STRICT POLICY
    # ======================================================

    environment = (
        plan.get("environment")
        or "production"
    )

    if (
        environment.lower() == "production"
        and total_changes > MAX_PRODUCTION_CHANGES
    ):

        return (
            "REJECT",
            (
                f"Production deployment contains "
                f"{total_changes} changes. "
                f"Maximum allowed for production is "
                f"{MAX_PRODUCTION_CHANGES}."
            )
        )

    # ======================================================
    # RULE 4
    # CRITICAL RESOURCE CHANGE = REJECT
    # ======================================================

    if critical_changes:

        return (
            "REJECT",
            (
                "Critical infrastructure resource(s) "
                "detected: "
                + ", ".join(critical_changes)
                + ". Automatic deployment is blocked."
            )
        )

    # ======================================================
    # RULE 5
    # SAFE CHANGE = APPROVE
    # ======================================================

    return (
        "APPROVE",
        (
            f"Plan passed all deployment policies. "
            f"Create={create_count}, "
            f"Update={update_count}, "
            f"Delete={delete_count}, "
            f"Total={total_changes}."
        )
    )
