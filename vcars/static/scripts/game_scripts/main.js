(function() {
    let isPause = false
    let animationId = null
    let speed = 3
    let score = 0
    let gameFinished = false
    const car = document.querySelector('.car')
    const carInfo = {
        ...createElementInfo(car),
        move: {
            top: null,
            bottom: null,
            left: null,
            right: null,
        },

    }
    const coin = document.querySelector('.coin')
    const coinInfo = createElementInfo(coin)
    const gameScore = document.querySelector('.game-score')
    const backdrop = document.querySelector('.backdrop')
    const restartButton = document.querySelector('.restart-button')
    const arrow = document.querySelector('.arrow')
    const arrowInfo = createElementInfo(arrow)
    const danger = document.querySelector('.danger')
    const dangerInfo = createElementInfo(danger)

    function createElementInfo(element) {
        return {
            width: element.clientWidth / 2,
            height: element.clientHeight,
            coords: getCoords(element),
            visible: true,
            ignoreAppearance: false,

        }
    }

    document.addEventListener('keydown', (event) => {
        if (isPause || gameFinished) {
            return
        }
        const code = event.code
        if ((code === 'ArrowUp' || code === 'KeyW') && carInfo.move.top === null) {
            if (carInfo.move.down) {
                return
            }
            carInfo.move.top = requestAnimationFrame(carMoveToTop(car, carInfo))
        } else if ((code === 'ArrowDown' || code === 'KeyS') && carInfo.move.bottom === null) {
            if (carInfo.move.top) {
                return
            }
            carInfo.move.bottom = requestAnimationFrame(carMoveToBottom(car, carInfo))
        } else if ((code === 'ArrowLeft' || code === 'KeyA') && carInfo.move.left === null) {
            if (carInfo.move.right) {
                return
            }
            carInfo.move.left = requestAnimationFrame(carMoveToLeft(car, carInfo))
        } else if ((code === 'ArrowRight' || code === 'KeyD') && carInfo.move.right === null) {
            if (carInfo.move.left) {
                return
            }
            carInfo.move.right = requestAnimationFrame(carMoveToRight(car, carInfo))
        }
    })
    document.addEventListener('keyup', (event) => {
        const code = event.code
        if (code === 'ArrowUp' || code === 'KeyW') {
            cancelAnimationFrame(carInfo.move.top)
            carInfo.move.top = null
        } else if (code === 'ArrowDown' || code === 'KeyS') {
            cancelAnimationFrame(carInfo.move.bottom)
            carInfo.move.bottom = null

        } else if (code === 'ArrowLeft' || code === 'KeyA') {
            cancelAnimationFrame(carInfo.move.left)
            carInfo.move.left = null
        } else if (code === 'ArrowRight' || code === 'KeyD') {
            cancelAnimationFrame(carInfo.move.right)
            carInfo.move.right = null
        }

    })
    animationId = requestAnimationFrame(startGame)

    function startGame() {
        elementAnimation(danger,  dangerInfo,speed, -250)
        if (dangerInfo.visible && hasCollision(carInfo, dangerInfo)) {
            return finishGame()
        }
        spritesAnimation(speed)
        elementAnimation(coin,  coinInfo,speed, -100)
        if (coinInfo.visible && hasCollision(carInfo, coinInfo)) {
            score += 1
            gameScore.innerText = score
            coin.style.display = 'none'
            coinInfo.visible = false
            if (score % 5 === 0) {
                speed += 1
            }
        }

        elementAnimation(arrow, arrowInfo, speed,-600)
        if (arrowInfo.visible && hasCollision(carInfo, arrowInfo)) {
            arrow.style.display = 'none'
            arrowInfo.visible = false
            danger.style.opacity = 0.5
            dangerInfo.visible = false
            arrowInfo.ignoreAppearance = true
            dangerInfo.ignoreAppearance = true
            speed += 10
            setTimeout(() => {
                danger.style.opacity = 1
                speed -= 10
                setTimeout(() => {
                    dangerInfo.visible = true
                    arrowInfo.ignoreAppearance = false
                    dangerInfo.ignoreAppearance = false
                }, 500)
            }, 1000)
        }
        animationId = requestAnimationFrame(startGame)
    }

    function cancelAnimations() {
        cancelAnimationFrame(animationId)
        cancelAnimationFrame(carInfo.move.top)
        cancelAnimationFrame(carInfo.move.bottom)
        cancelAnimationFrame(carInfo.move.left)
        cancelAnimationFrame(carInfo.move.right)
    }

    function finishGame() {
        gameFinished = true
        cancelAnimations()
        gameScore.style.display = 'none'
        gameButton.style.display = 'none'
        backdrop.style.display = 'flex';
        const scoreText = backdrop.querySelector('.finish-text-score')
        scoreText.innerText = score

    }

    const gameButton = document.querySelector('.game-button')
    gameButton.addEventListener('click', () => {
        isPause = !isPause;
        if (isPause) {
            cancelAnimations()
            gameButton.children[0].style.display = 'none'
            gameButton.children[1].style.display = 'initial'
        } else {
            aminationId = requestAnimationFrame(startGame)
            gameButton.children[0].style.display = 'initial'
            gameButton.children[1].style.display = 'none'
        }
    })
    restartButton.addEventListener('click', () => {
        window.location.reload()
    })
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.code === 'F5') {
            event.preventDefault()
        }
    })
})()