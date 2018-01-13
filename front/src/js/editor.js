if (!localStorage.getItem('history'))
  localStorage.setItem('history', '{ "sto": [], "dbp": [] }')

updateHistory(null, null)

function ontologyChange() {
  var ontology = document.getElementById('ontology').value
  updateHistory(null, ontology)
}

function sendQuery() {
  var ontology = document.getElementById('ontology').value

  var query = document.getElementById('query').value
  var headlinesStartIndex = query.toLowerCase().search('select')
  var headlinesEndIndex = query.toLowerCase().search('where')
  if (headlinesEndIndex === -1)
    headlinesEndIndex = query.toLowerCase().search('{')
  var headlines = query.substring(headlinesStartIndex, headlinesEndIndex).split(" ")
  headlines.pop()
  headlines.shift()
  for (var i = 0; i < headlines.length; i++) {
    if (headlines[i] === 'distinct') {
      headlines.splice(i, 1)
      i = i - 1
    } else {
      headlines[i] = headlines[i].replace('?','')
    }
  }

  addToHistory(query, ontology)
  document.getElementById('spinner').style.display = 'initial'
  postRequest('/query', { type: 'query', quer: query, ont: ontology, head: headlines })
}

function responseHandler(response) {
  if (response.type === 'query') {
    document.getElementById('spinner').style.display = 'none'
    // document.getElementById('queryResult').style.display = 'initial'
    // document.getElementById('queryResultInfo').style.display = 'flex'
  
    var ontology = response.ont
    if (ontology === 'dbp')
      var content = Object.keys(response.data).map((k) => {
        var arr = []
        for (let prop in response.data[k]) 
          if (response.data[k].hasOwnProperty(prop))
            arr.push(response.data[k][prop]['value'])
        return arr
      })
    else if (ontology === 'sto')
      var content = response.data
    else
      console.log('Unknown ontology!')
  
    document.getElementById('queryResult').innerHTML = createTable(response.heads, content)
    document.getElementById('rowsNum').innerHTML = content.length
    document.getElementById('colsNum').innerHTML = content[0].length
  } else if (response.type === 'update') {
    console.log(response.result)
  } else {
    console.log('Unknown response type!')
  }
}

function createTable(headlines, content) {
  var tableHTML = '<table class="query-result-table">'
  tableHTML += '<tr>'
  headlines.forEach(headline =>{
    tableHTML += '<td><b>' + headline + '</b></td>'
  })
  tableHTML += '</tr>'
  content.forEach(rowData => {
    tableHTML += '<tr>'
    rowData.forEach(cellData => {
      tableHTML += '<td>' + cellData + '</td>'
    })
    tableHTML += '</tr>'
  })
  tableHTML += '</table>'
  return tableHTML
}

function addToHistory(query, ontology) {
  var history = JSON.parse(localStorage.getItem('history'))
  if (history[ontology].length < 10) {
    history[ontology].push(query)
  } else {
    history[ontology].shift()
    history[ontology].push(query)
  }
  localStorage.setItem('history', JSON.stringify(history))

  updateHistory(history, ontology)
}

function updateHistory(history, ontology) {
  if (history === null)
    history = JSON.parse(localStorage.getItem('history'))
  if (ontology === null)
    ontology = document.getElementById('ontology').value

  html = '<table class="fav-table">'
  history[ontology].reverse().forEach((query, index) => {
    html += '<tr style="cursor: pointer;" onclick="queryClick(\'' + ontology +
      ':' + index + '\')"><td>' + query.substring(0,30) + '...</td></tr>'
  })
  html += '</table>'
  document.getElementById('queryStack').innerHTML = html
}

function queryClick(value) {
  var ontology = value.split(':')[0]
  var index = value.split(':')[1]
  var queryObj = JSON.parse(localStorage.getItem('history'))
  var query = queryObj[ontology].reverse()[index]
  document.getElementById('query').value = query
}

function addTriple() {
  subject = document.getElementById('subj').value
  predicate = document.getElementById('pred').value
  object = document.getElementById('obj').value
  
  postRequest('/update', { type: 'update', subj: subject, pred: predicate, obj: object })
}

function querySlider() {
  console.log('querySlider')
}

function addTripleSlider() {
  console.log('addTripleSlider')
}
