/* globals Request */

const Cookies = require('js-cookie')

function getRandomCard (stackPk) {
  return new Request(`/json/stacks/${stackPk}/random-card/`, { 'credentials': 'include' })
}

function postCardResults (cardPk, correct) {
  const csrftoken = Cookies.get('csrftoken')
  return new Request(`/json/card-results/${cardPk}/`, {
    credentials: 'include',
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({ 'correct': correct })
  })
}

module.exports = {
  'getRandomCard': getRandomCard,
  'postCardResults': postCardResults
}
