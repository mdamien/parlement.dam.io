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
        <div style="padding: 0 10px; color:rgb(136, 153, 166)" id="filters">
            <span style="border-bottom: 2px solid rgb(29, 161, 242);color:rgb(29, 161, 242)">
                <b>Tout</b>
            </span>
            <span>
                Votes
            </span>
            <span>
                Interventions
            </span>
            <span>
                Amendements
            </span>
            <span>
                Propositions de loi
            </span>
            <span>
                Questions orales
            </span>
            <span>
                Questions écrites
            </span>
            <span>
                Rapports
            </span>
        </div>
        <hr style="border:none; border-top: 1px solid #38444d">
        [events]
    </div>
    <style>
        html {min-height: 100%}
        #filters > span {
            display: inline-block;
            padding: 10px;
            cursor: pointer;
        }
    </style>
</body>
"""

def render(events):
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
    return TEMPLATE.replace('[events]', events_html)