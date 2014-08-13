import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
from pyes import *
from collections import Counter

conn = ES('http://192.168.56.101:9200/')
start_page = 1
items_per_page = 5000
# I need to figure out pagination at some point, this will likely die horribly


def fileFormatLister(hitman):
  # currently this only takes file format from file utility output since it has the most human-readable results compared to NLNZ and Tika. Misty@Artefactual has suggested that this data will be removed from ElasticSearch sometime soon in favour of just putting it in the actual METS file, which I can manage to query when that happens, but this will need to be rewritten to navigate XML.
  amdSecElementNum = 0
  fileFormats = []
  for x in hitman._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list']:
    if amdSecElementNum < len(hitman._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list']) - 1:
      try:
        fileFormats.append( x[u'ns0:techMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns2:object_list'][0][u'ns2:objectCharacteristics_list'][0][u'ns2:objectCharacteristicsExtension_list'][0][u'ns3:fits_list'][0][u'ns3:identification_list'][0][u'ns3:identity_list'][0][u'@format'])
      except:
        try:
          fileFormats.append( x[u'ns0:techMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns3:object_list'][0][u'ns3:objectCharacteristics_list'][0][u'ns3:objectCharacteristicsExtension_list'][0][u'ns4:fits_list'][0][u'ns4:identification_list'][0][u'ns4:identity_list'][0][u'@format'])
        except:
          pass
    amdSecElementNum += 1
  return fileFormats


def AIPsummary():
  q = StringQuery('*')

  try:
    results = conn.search_raw(
      query=q,
      indices='aips',
      type='aip'
    )
  except:
    pass

  if results:

    totalAIPs = len(results.hits.hits)
    totalAIPsize = 0

    allFileFormats = []
    ingestDates = []
    for x in results.hits.hits:
      totalAIPsize += x._source.size
      allFileFormats.extend(fileFormatLister(x))

      try:
        # no idea why this needs ns2 sometimes and ns3 sometimes. doesn't seem like it's arbitrarily incremented but definitely seems arbitrary. need to fix.
        ingestDates.append( str(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list'][0][u'ns0:digiprovMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns2:event_list'][0][u'ns2:eventDateTime'].month) + "-" + str(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list'][0][u'ns0:digiprovMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns2:event_list'][0][u'ns2:eventDateTime'].year))
      except:
        ingestDates.append( str(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list'][0][u'ns0:digiprovMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns3:event_list'][0][u'ns3:eventDateTime'].month) + "-" + str(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:amdSec_list'][0][u'ns0:digiprovMD_list'][0][u'ns0:mdWrap_list'][0][u'ns0:xmlData_list'][0][u'ns3:event_list'][0][u'ns3:eventDateTime'].year))

    totalFiles = len(allFileFormats)
    fileFormatCounts = Counter(allFileFormats)
    ingestDateCounts = Counter(ingestDates)
    totalAIPsizeMB = '%.2f' % totalAIPsize
    averageAIPsizeMB = '%.2f' % (totalAIPsize/len(results.hits.hits))

    return ( totalAIPs, totalFiles, fileFormatCounts, ingestDateCounts, totalAIPsizeMB, averageAIPsizeMB )


#UUID = "eDRn6BomQFaMP6TCZm9VhA"

def AIPproperties(UUID):
  q = TermQuery("_id", UUID)

  try:
    results = conn.search_raw(
      query=q,
      indices='aips',
      type='aip'
    )
  except:
    pass

  if results.hits.hits:
    size = '%.2f' % results.hits.hits[0]._source.size
    #numFiles = len(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:fileSec_list'][0][u'ns0:fileGrp_list']) - 1
    fileFormatList = fileFormatLister(results.hits.hits[0])
    numFiles = len(fileFormatList)
    fileFormatCounts = Counter(fileFormatList)
    #fileFormatCounts = Counter(fileFormatLister(results.hits.hits[0]))
    return (size,numFiles,fileFormatCounts,1)

  else:
    q = TermQuery("uuid", UUID)

    try:
      results = conn.search_raw(
        query=q,
        indices='aips',
        type='aip'
        )
    except:
      pass

    if results.hits.hits:
      size = '%.2f' % results.hits.hits[0]._source.size
      #numFiles = len(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:fileSec_list'][0][u'ns0:fileGrp_list']) - 1
      fileFormatList = fileFormatLister(results.hits.hits[0])
      numFiles = len(fileFormatList)
      fileFormatCounts = Counter(fileFormatList)
      #fileFormatCounts = Counter(fileFormatLister(results.hits.hits[0]))
      return (size,numFiles,fileFormatCounts,1)

    else:
      q = TermQuery("name", UUID)

      try:
        results = conn.search_raw(
          query=q,
          indices='aips',
          type='aip'
          )
      except:
        pass

      if results.hits.hits:
        size = '%.2f' % results.hits.hits[0]._source.size
        #numFiles = len(results.hits.hits[0]._source.mets[u'ns0:mets_list'][0][u'ns0:fileSec_list'][0][u'ns0:fileGrp_list']) - 1
        fileFormatList = fileFormatLister(results.hits.hits[0])
        numFiles = len(fileFormatList)
        fileFormatCounts = Counter(fileFormatList)
        #fileFormatCounts = Counter(fileFormatLister(results.hits.hits[0]))
        return (size,numFiles,fileFormatCounts,1)

      else:
        return (0,0,0,0)


def unprocessedTransfers():
  q = StringQuery('*')

  try:
    results = conn.search_raw(
      query=q,
      indices='transfers',
      type='transferfile'
    )
  except:
    pass

  if results:

    sipUUIDs = []
    for x in results.hits.hits:
      sipUUIDs.append(x._source.sipuuid)
    totalTransfers = len(list(set(sipUUIDs)))
  # unfortunately it's hard for me to get much other than a total number of unprocessed transfers because elasticsearch seems to be used primarily for AIPs. I'll have to take a look to see if the remainder is in MySQL... took a look, can't find anything.
    return totalTransfers
