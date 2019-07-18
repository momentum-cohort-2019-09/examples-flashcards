/* globals fetch */

const $ = require('jquery')
const requests = require('./requests')

setupFlashcard()
setupVocabFlashcard()
setupShowAnswerButton()

function getRandomCard ($cardEl) {
  const stackPk = $cardEl.data('stack-pk')
  return fetch(requests.getRandomCard(stackPk))
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
  const $cardEl = $('#card')

  if ($cardEl.length === 0) { return }

  getRandomCard($cardEl)

  for (let form of document.querySelectorAll('.post-answer-form')) {
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      const cardPk = $cardEl.data('card-pk')
      const answerIsCorrect = form.dataset.correct === 'true'

      fetch(requests.postCardResults(cardPk, answerIsCorrect))
        .then(() => $('.flip-container').toggleClass('flipped'))
        .then(() => getRandomCard($cardEl))
    })
  }
}

function getRandomVocabWord ($cardEl) {
  return fetch(requests.getRandomVocab())
    .then(res => res.json())
    .then(function (data) {
      $('#card-prompt').text(data.word)
      $('#card-answer').html(`<ul>${data.definitions.map(d => `<li>${d}</li>`).join('')}</ul>`)
    })
}

function setupVocabFlashcard () {
  const $cardEl = $('#vocab-card')

  if ($cardEl.length === 0) { return }

  getRandomVocabWord($cardEl)

  for (let form of document.querySelectorAll('.post-answer-form')) {
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      // const answerIsCorrect = form.dataset.correct === 'true'
      $('.flip-container').toggleClass('flipped')
      getRandomVocabWord($cardEl)
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
