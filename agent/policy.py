def evaluate_policy(plan):

    changes = plan.get("resource_changes", [])

    create_count = 0
    update_count = 0
    delete_count = 0

    for resource in changes:

        actions = resource.get("change", {}).get("actions", [])

        if "create" in actions:
            create_count += 1

        if "update" in actions:
            update_count += 1

        if "delete" in actions:
            delete_count += 1

    print("------------------------------------")
    print("Terraform Plan Analysis")
    print("------------------------------------")

    print(f"Create : {create_count}")
    print(f"Update : {update_count}")
    print(f"Delete : {delete_count}")

    # ==========================================
    # POLICY 1
    # Don't automatically approve destruction
    # ==========================================

    if delete_count > 0:

        return (
            "REJECT",
            f"Terraform plan contains {delete_count} resource deletion(s)."
        )

    # ==========================================
    # POLICY 2
    # Too many changes
    # ==========================================

    total_changes = (
        create_count +
        update_count +
        delete_count
    )

    if total_changes > 20:

        return (
            "REJECT",
            f"Too many infrastructure changes: {total_changes}."
        )

    # ==========================================
    # POLICY 3
    # Everything looks safe
    # ==========================================

    return (
        "APPROVE",
        (
            f"Plan approved. "
            f"Create={create_count}, "
            f"Update={update_count}, "
            f"Delete={delete_count}."
        )
    )