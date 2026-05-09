from raspberry_monitor_ha import base_classes, callbacks

configured_buttons = [
    base_classes.create_button(
        name="Restart_RP_monitoring",
        callback_func=callbacks.restart_service
    ),
    base_classes.create_button(
        name="Shutdown_Machine",
        callback_func=callbacks.shutdown_machine,
        icon="mdi:power"
    )
]