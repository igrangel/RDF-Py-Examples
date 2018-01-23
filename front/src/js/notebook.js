sessionStorage.setItem('notebooks', '[]')

function newNotebook() {
  notebooks = JSON.parse(sessionStorage.getItem('notebooks'))
  num = notebooks.length
  if (num > 0)
    notebooks[notebooks.length - 1].replace('queryResult', 'queryResult' + num)
  newNotebook =
  '<div class="query-form">' +
    '<select id="ontology" onchange="ontologyChange()">' +
      '<option value="sto">Standard Ontology</option>' +
      '<option value="dbp">DBpedia</option>' +
    '</select>' +
    '<div style="display: flex; flex-direction: row;">' +
      '<textarea id="query" rows="10" cols="45" name="text" class="query-textarea"></textarea>' +
    '</div>' +
    '<button onclick="sendQuery()">send query</button>' +
  '</div>' +
  '<img src="img/spinner.gif" id="spinner" class="spinner" />' +
  '<div id="queryResult" class="query-result"></div>' +
  '<div id="queryResultInfo" class="query-result-info">' +
  '<span>number of rows: <span id="rowsNum">0</span></span>' +
  '<span>number of cols: <span id="colsNum">0</span></span>' +
  '</div>'
  document.getElementById('sContent').innerHTML += newNotebook
  notebooks.push(newNotebook)
  sessionStorage.setItem('notebooks', notebooks)
}


function ontologyChange() {
  var ontology = document.getElementById('ontology').value
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
