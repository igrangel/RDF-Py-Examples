$( document ).ready(() => {
  menuEl = window.location.pathname.substr(1, window.location.pathname.length-1);
  $("#headPC").load("head-pc.html", () => $('#' + menuEl + 'PC').addClass('s-curr-p'));
  $("#headMobile").load("head-mobile.html", () => $('#'+ menuEl + 'Mobile').addClass('s-curr-m'));
})

function getRequest(url) {
  axios.get(url)
    .then(function(response) {
      console.log('Requested data: ', response.data)
    })
    .catch(function(error) {
      console.log('Error: ', error);
    });
}

function postRequest(url, params) {
  axios.post(url, params)
    .then(function(response) {
      // console.log('Requested data: ', response.data)
      responseHandler(response.data)
    })
    .catch(function(error) {
      console.log('Error: ', error);
    });
}

function legendClick() {
  var display = document.getElementById('s-img-close').style.display
  if (display === 'none' || display === '') {
    document.getElementById('s-img-menu').style.display = 'none'
    document.getElementById('s-img-close').style.display = 'initial'
    document.getElementById('s-side-menu').style.marginLeft = '0'
    document.getElementById('s-legend').style.backgroundColor = '#218c86'
  } else {
    document.getElementById('s-img-close').style.display = 'none'
    document.getElementById('s-img-menu').style.display = 'initial'
    document.getElementById('s-side-menu').style.marginLeft = '-302px'
    document.getElementById('s-legend').style.backgroundColor = 'lightseagreen'
  }
}
