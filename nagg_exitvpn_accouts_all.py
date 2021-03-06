#!/usr/bin/env python3

def nagg_exitvpn_accouts():
    from common import pinit
    from datetime import datetime, timedelta

    photon, settings = pinit('nagg_exitvpn_accouts', verbose=True)

    # initialize the gateway-configs repo ...
    photon.git_handler(
        settings['configs']['local'],
        remote_url=settings['configs']['remote']
    )

    # .. to load contents from the exitvpn.yaml into the settings
    if not photon.settings.load('exitvpn', settings['configs']['exitvpn']):
        photon.m(
            'could not load exitvpn from git',
            more=dict(
                exitvpn=settings['configs']['exitvpn']
            ),
            state=True
        )
    photon.s2m

    res=dict(overdue=list(), warning=list(), good=list())
    now = datetime.now()

    for gateway in sorted(settings['exitvpn']['gateways'].keys()):
        if settings['exitvpn']['gateways'][gateway].get('until'):
            until = datetime.strptime(settings['exitvpn']['gateways'][gateway]['until'], settings['exitvpn']['conf']['date_format'])
            delta = until - now
            f = 'overdue' if delta <= timedelta(days=0) else 'warning' if delta <= timedelta(days=settings['exitvpn']['conf']['warndays']) else 'good'
            res[f].append({
                gateway: settings['exitvpn']['gateways'][gateway]
            })

    photon.m('results', more=res)

    if now.weekday() == settings['exitvpn']['conf']['digestday'] or res['warning']:
        punchline = 'Achtung! VPN Account läuft aus' if res['warning'] else 'VPN Wochenbericht'
        mail = photon.mail_handler(
            to=settings['common']['mailto']['admin'],
            cc=settings['common']['mailto']['kontakt'],
            sender=settings['common']['mailto']['local'],
            subject='photon exitVPN notify',
            punchline=punchline,
            add_settings=False
        )
        mail.text = ''
        mail.text = res
        mail.text = 'Do not forget to update the exitvpn.yaml ( https://github.com/freifunk-mwu/gateway-configs.git )'
        mail.text = ''
        mail.send

if __name__ == '__main__':
    nagg_exitvpn_accouts()
