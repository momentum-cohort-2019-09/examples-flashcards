/* globals fetch */

const cardEl = document.querySelector('#card')

if (cardEl) {
  const stackPk = cardEl.dataset.stackPk
  console.log('stackPk', stackPk)
  const req = new Request(`/json/stacks/${stackPk}/random-card/`, { 'credentials': 'include' })
  fetch(req)
    .then(res => res.json())
    .then(function (data) {
      const card = data.card
      document.querySelector('#card-prompt').innerText = card.prompt
      document.querySelector('#card-answer').innerText = card.answer
    })
}

const showAnswerLink = document.querySelector('#show-answer-link')

if (showAnswerLink) {
  showAnswerLink.addEventListener('click', function (event) {
    event.preventDefault()

    document.querySelector('.flip-container').classList.toggle('flipped')
  })
}
