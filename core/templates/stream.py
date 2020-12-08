import locale

from lys import L


TEMPLATE = """
<title>Actualités de YYY</title>
<body style="background: #15202b; min-height: 100%;color:white; font-family: sans-serif;margin: 0">
    <style>
        html {min-height: 100%}
        a {
            color: inherit;
            text-decoration: none;
        }
        #filters > a {
            display: inline-block;
            padding: 10px;
        }
        #filters > a:hover {
            color: rgb(29, 161, 242) !important;
            background: rgba(29, 161, 242, 0.1);
        }
        .post:hover {
            background: rgba(29, 161, 242, 0.1);
        }
    </style>
    <div style="margin: auto; border-left: 1px solid #38444d; border-right: 1px solid #38444d; max-width: 600px">
        <br>
        <center>Actualités des parlementaires</center>
        <br>
        <hr style="border:none; border-top: 1px solid #38444d;margin:0">
        <div style="padding: 0 10px">
            <span style="float: right;">
                <button onclick='follow()'style="cursor:pointer;color:white;background: rgb(29, 161, 242); border: none; padding: 10px 20px; border-radius: 10px"><b>Suivre</b></button>
            </span>
            <p><img src="https://www.nosdeputes.fr/depute/photo/ZZZ" width=100 style="border-radius:10px"/></p>
            <p><b>YYY</b></p>
            <p>Député (XXX) - GGG</p>
        </div>
        <div style="color:rgb(136, 153, 166)" id="filters">
            [filters]
        </div>
        <hr style="border:none; border-top: 1px solid #38444d;margin:0">
        [events]
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
    <script>
    function follow() {
        mail = prompt('Adresse mail')
        $.post('/follow/', {
            slug: "ZZZ",
            email: mail,
            csrfmiddlewaretoken: "TTT",
        }, function() {
            alert('Vous êtes désormais abonné aux actualités de YYY')
        })
    }
    </script>
</body>
"""


def render(requests, events):
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

    events_html = ""
    for event in events:
        event_html = """
        <a href="[url]" style="padding: 10px 10px; display:block" class="post">
            <p style="color:rgb(136, 153, 166);margin: 0;padding-bottom:10px">[date] - [type]</p>
            [content]
        </a>
        <hr style="border:none; border-top: 1px solid #38444d;margin:0">
        """
        date = str(event['date'].strftime("%a %d %b %Y"))
        event_html = event_html.replace('[url]', event['url'])
        event_html = event_html.replace('[date]', date)
        event_html = event_html.replace('[type]', event['type'])
        event_html = event_html.replace('[content]', event['content'])
        events_html += event_html

    filters_html = ""
    filters = (
        ('?', 'Tout'),
        ('?filter=votes', 'Votes'),
        ('?filter=interventions', 'Interventions'),
        ('?filter=amendements', 'Amendements'),
        ('?filter=propositions-de-loi', 'Propositions de loi'),
        ('?filter=questions-orales', 'Questions orales'),
        ('?filter=questions-ecrites', 'Questions écrites'),
        ('?filter=rapports', 'Rapports'),
    )
    for filter_href, filter_text in filters:
        filter = None
        if '=' in filter_href:
            filter = filter_href.split('=')[1]
        style = None
        if requests.GET.get('filter') == filter:
            style="border-bottom: 2px solid rgb(29, 161, 242);color:rgb(29, 161, 242)"
        filters_html += str(L.a(href=filter_href, style=style) / filter_text)

    html = TEMPLATE.replace('[events]', events_html)
    html = html.replace('[filters]', filters_html)

    return html