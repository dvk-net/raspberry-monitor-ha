from raspbery_monitor_ha import base_classes, callbacks

configured_buttons = [
    base_classes.create_button(
        name="Restart_RP_monitoring",
        callback_func=callbacks.restart_service
    )
]