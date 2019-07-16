/* globals fetch, Cookies, Request */

setupFlashcard()
setupShowAnswerButton()

function getRandomCard (cardEl) {
  const stackPk = cardEl.dataset.stackPk
  console.log('stackPk', stackPk)
  const req = new Request(`/json/stacks/${stackPk}/random-card/`, { 'credentials': 'include' })
  return fetch(req)
    .then(res => res.json())
    .then(function (data) {
      const card = data.card
      cardEl.dataset.cardPk = card.pk
      document.querySelector('#card-prompt').innerText = card.prompt
      document.querySelector('#card-answer').innerText = card.answer
    })
}

function setupFlashcard () {
  const cardEl = document.querySelector('#card')

  if (!cardEl) { return }

  getRandomCard(cardEl)

  for (let form of document.querySelectorAll('.post-answer-form')) {
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      const csrftoken = Cookies.get('csrftoken')
      const cardPk = cardEl.dataset.cardPk
      const answerIsCorrect = form.dataset.correct === 'true'
      const req = new Request(`/json/card-results/${cardPk}/`, {
        credentials: 'include',
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'correct': answerIsCorrect })
      })
      fetch(req)
        .then(res => res.json())
        .then(function (data) {
          console.log('data', data)
        })
        .then(() => document.querySelector('.flip-container').classList.toggle('flipped'))
        .then(() => getRandomCard(cardEl))
    })
  }
}

function setupShowAnswerButton () {
  const showAnswerLink = document.querySelector('#show-answer-link')

  if (!showAnswerLink) { return }
  showAnswerLink.addEventListener('click', function (event) {
    event.preventDefault()

    document.querySelector('.flip-container').classList.toggle('flipped')
  })
}
