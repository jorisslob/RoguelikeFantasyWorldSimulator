import tdl


def handle_keys(fov_recompute, player, the_map):
    # realtime
    keypress = False
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            keypress = True

    if not keypress:
        return (False, fov_recompute)

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return (True, False)  # exit game

    # movement keys
    if user_input.key == 'UP':
        player.move(0, -1, the_map)
        fov_recompute = True

    elif user_input.key == 'DOWN':
        player.move(0, 1, the_map)
        fov_recompute = True

    elif user_input.key == 'LEFT':
        player.move(-1, 0, the_map)
        fov_recompute = True

    elif user_input.key == 'RIGHT':
        player.move(1, 0, the_map)
        fov_recompute = True

    return (False, fov_recompute)
