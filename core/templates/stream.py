from lys import L


TEMPLATE = """
<body style="background: #15202b; min-height: 100%;color:white; font-family: sans-serif;margin: 0">
    <div style="margin: auto; border-left: 1px solid #38444d; border-right: 1px solid #38444d; max-width: 600px">
        <br>
        <center>parlement.dam.io</center>
        <hr style="border:none; border-top: 1px solid #38444d">
        <div style="padding: 0 10px">
            <br>
            <span style="float: right;">
                <button style="color:white;background: rgb(29, 161, 242); border: none; padding: 10px 20px; border-radius: 10px"><b>Suivre</b></button>
            </span>
            <p><b>Paula Forteza</b></p>
            <p>Député (XXX)</p>
        </div>
        <div style="color:rgb(136, 153, 166)" id="filters">
            [filters]
        </div>
        <hr style="border:none; border-top: 1px solid #38444d">
        [events]
    </div>
    <style>
        html {min-height: 100%}
        #filters > a {
            display: inline-block;
            padding: 10px;
            color: inherit;
            text-decoration: none;
        }
        #filters > a:hover {
            color: rgb(29, 161, 242) !important;
            background: rgba(29, 161, 242, 0.1);
        }
    </style>
</body>
"""


def render(requests, events):
    events_html = ""
    for event in events:
        event_html = """
        <div style="padding: 0 10px">
            <p style="color:rgb(136, 153, 166)">[date] - [type]</p>
            [content]
        </div>
        <hr style="border:none; border-top: 1px solid #38444d">
        """
        event_html = event_html.replace('[date]', event['date'])
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