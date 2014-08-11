from bottle import get, post, request, run
import querying
from collections import Counter

@get('/reports')
def queryfields():
    return '''
        <h1>Archivematica Reporting Tool</h1>
        <form action="/reports" method="post">
            AIP name or UUID: <input name="UUID" type="text" />
            <input value="query" type="submit" />
        </form>
        <form action="/summary" method="get">
            or, get a <input value="summary" type="submit" /> of AIP statistics
        </form>
        <form action="/unprocessed" method="get">
            or, find out how many <input value="unprocessed transfers" type="submit" /> there are
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
        return "<p>No results found. May not be a valid UUID.</p>"

#    if querying.AIPproperties(UUID) != 1:
#        return "<p>AIP size:"+size+"</p><p>total number of files in AIP:"+numFiles+"</p><p>tally of file formats:"+fileFormatCounts+"</p>"
#    else:
#        return "<p>No results found. May not be a valid UUID.</p>"

@get('/summary')
def do_summary():
    summaryData = querying.AIPsummary()
    tallyRows = ""
    for fileTally in summaryData[2].most_common():
      tallyRows += str("<tr><td>"+str(fileTally[0])+"</td><td>"+str(fileTally[1])+"</td></tr>")
    return "<h1>summary of AIPs</h1><p>total AIPs: "+str(summaryData[0])+"</p><p>total files across all AIPS: "+str(summaryData[1])+"</p><p>tally of file formats:</p><p><table cellspacing='10'>"+tallyRows+"</table></p><p>ingest statistics, by month: "+str(summaryData[3])+"</p><p>total size of all AIPs: "+str(summaryData[4])+" MB</p><p>average AIP size: "+str(summaryData[5])+" MB</p>"

#    querying.AIPsummary()
#    return "<p>total AIPs:"+totalAIPs+"</p><p>total files across all AIPS:"+totalFiles+"</p><p>tally of file formats:"+fileFormatCounts+"</p><p>ingest statistics, by month:"+ingestDateCounts+"</p><p>total size of all AIPs, in MB"+totalAIPsizeMB+"</p><p>average AIP size, in MB"+averageAIPsizeMB+"</p>"

@get('/unprocessed')
def do_unprocessed():
    unprocessedTransferData = querying.unprocessedTransfers()
    return str(unprocessedTransferData)+" unprocessed transfers currently"

#    querying.unprocessedTransfers()
#    return totalTransfers+" unprocessed transfers currently"

run(host='0.0.0.0', port=8080, debug=True)
