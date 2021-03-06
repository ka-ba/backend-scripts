#!/usr/bin/env python3

BLOCK = '''
\t<div class="block"><a href="{href}">{text}</a></div>
'''

SYSBLOCK = '''
\t<div class="block" onclick="toggle('{command_tag}')">
\t\t<h2>{command}</h2>
\t\t<div class="cblock" id="{command_tag}">
\t\t\t<pre>{cmd_output}</pre>
\t\t</div>
\t</div>
'''

def gen_website():
    from os import path
    from common import pinit
    from common.html import page

    photon, settings = pinit('gen_website', verbose=True)

    main = ''
    if path.exists(path.join(settings['web']['output'], 'firmware')):
        main += BLOCK.format(href='firmware', text='Firmware')

    if path.exists(path.join(settings['web']['output'], '_archive')):
        main += BLOCK.format(href='_archive', text='Firmware Archive')

    if path.exists(path.join(settings['web']['output'], 'traffic')):
        main += BLOCK.format(href='traffic', text='Traffic')

    main += BLOCK.format(href='system', text='System Statistics')

    page(photon, main)

    sys = '<small>click to show or hide</small><br />'
    for command in settings['web']['system']:
        cmd_output = photon.m(
            'retrieving system info',
            cmdd=dict(cmd=command),
            critical=False
        ).get('out')
        sys += SYSBLOCK.format(command=command, command_tag=command.split()[0], cmd_output=cmd_output)

    page(photon, sys, sub='system')


if __name__ == '__main__':
    gen_website()
