/* globals fetch, Request */

const Cookies = require('js-cookie')
const $ = require('jquery')

setupFlashcard()
setupShowAnswerButton()

function getRandomCard ($cardEl) {
  const stackPk = $cardEl.data('stack-pk')
  console.log('stackPk', stackPk)
  const req = new Request(`/json/stacks/${stackPk}/random-card/`, { 'credentials': 'include' })
  return fetch(req)
    .then(res => res.json())
    .then(function (data) {
      const card = data.card
      $cardEl.data('card-pk', card.pk)
      $('#card-prompt').text(card.prompt)
      $('#card-answer').text(card.answer)
      $('#times-answered').text(card.times_answered)
      $('#times-correct').text(card.times_correct)
      $('#times-incorrect').text(card.times_incorrect)
      $('#last-answered-at').text(card.last_answered_at)
      $('#answer-count').text(card.answer_count)
    })
}

function setupFlashcard () {
  // const cardEl = document.querySelector('#card')
  const $cardEl = $('#card')

  if ($cardEl.length === 0) { return }

  getRandomCard($cardEl)

  for (let form of document.querySelectorAll('.post-answer-form')) {
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      const csrftoken = Cookies.get('csrftoken')
      const cardPk = $cardEl.data('card-pk')
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
        .then(() => $('.flip-container').toggleClass('flipped'))
        .then(() => getRandomCard($cardEl))
    })
  }
}

function setupShowAnswerButton () {
  const $showAnswerLink = $('#show-answer-link')

  if ($showAnswerLink.length === 0) { return }
  $showAnswerLink.on('click', function (event) {
    event.preventDefault()

    $('.flip-container').toggleClass('flipped')
  })
}
