from bottle import get, post, request, run
import querying
from collections import Counter

@get('/reports')
def queryfields():
    return '''
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <h1>&nbsp;&nbsp;Archivematica Reporting Tool</h1>
        <form action="/reports" method="post">
            &nbsp;&nbsp;AIP name or UUID: <input name="UUID" type="text" />
            <input value="query" type="submit" />
        </form>
        <form action="/summary" method="get">
            &nbsp;&nbsp;or, get a <input value="summary" type="submit" /> of AIP statistics
        </form>
        <form action="/unprocessed" method="get">
            &nbsp;&nbsp;or, find out how many <input value="unprocessed transfers" type="submit" /> there are
        </form>
    '''

@post('/reports')
def do_query():
    UUID = request.forms.get('UUID')
    AIPpropertyData = querying.AIPproperties(UUID)
    if AIPpropertyData[3] == 1:
        tallyRows = ""
        for fileTally in AIPpropertyData[2].most_common():
          tallyRows += str("<tr><td>"+str(fileTally[0])+"</td><td>"+str(fileTally[1])+"</td></tr>")
        return "<h1>summary for AIP "+UUID+"</h1><p>AIP size: "+str(AIPpropertyData[0])+" MB</p><p>total number of files in AIP: "+str(AIPpropertyData[1])+"</p><p>tally of file formats:</p><p><table cellspacing='10'>"+tallyRows+"</table></p>"
    else:
        return "<p>No results found. May not be a valid UUID or AIP name.</p>"

@get('/summary')
def do_summary():
    summaryData = querying.AIPsummary()
    formatTallyRows = ""
    for fileTally in summaryData[2].most_common():
      formatTallyRows += str("<tr><td>"+str(fileTally[0])+"</td><td>"+str(fileTally[1])+"</td></tr>")
    dateTallyRows = ""
    for dateTally in summaryData[3].most_common():
      dateTallyRows += str("<tr><td>"+str(dateTally[0])+"</td><td>"+str(dateTally[1])+"</td></tr>")
    return "<h1>summary of AIPs</h1><p>total AIPs: "+str(summaryData[0])+"</p><p>total files across all AIPS: "+str(summaryData[1])+"</p><p>tally of file formats:</p><p><table cellspacing='10'>"+formatTallyRows+"</table></p><p>ingest statistics, by month:</p><p><table cellspacing='10'>"+dateTallyRows+"</table></p><p>total size of all AIPs: "+str(summaryData[4])+" MB</p><p>average AIP size: "+str(summaryData[5])+" MB</p>"

@get('/unprocessed')
def do_unprocessed():
    unprocessedTransferData = querying.unprocessedTransfers()
    return str(unprocessedTransferData)+" unprocessed transfers currently"

run(host='0.0.0.0', port=8080, debug=True)
