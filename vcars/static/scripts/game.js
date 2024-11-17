(function () {
    let isPause = false
    let animationId = null
    let speed = 3
    let score = 0
    const car = document.querySelector('.car')
    const carInfo = {
        width: car.clientWidth / 2,
        height: car.clientHeight,
        coords: getCoords(car),
        move: {
            top: null,
            bottom: null,
            left: null,
            right: null,
        },
        visible: true,

    }
    const coin = document.querySelector('.coin')
    const coinInfo = {
        width: coin.clientWidth / 2,
        height: coin.clientHeight,
        coords: getCoords(coin),
        visible: true,
    }
    const gameScore = document.querySelector('.game-score')
    const backdrop = document.querySelector('.backdrop')
    const restartButton = document.querySelector('.restart-button')
    const arrow = document.querySelector('.arrow')
    const arrowInfo = {
        width: arrow.clientWidth / 2,
        height: arrow.clientHeight,
        coords: getCoords(arrow),
        visible: true,
    }
    const danger = document.querySelector('.danger')
    const dangerInfo = {
        width: danger.clientWidth / 2,
        height: danger.clientHeight,
        coords: getCoords(danger),
        visible: true,
    }

    const road = document.querySelector('.road')
    const roadHeight = road.clientHeight
    const roadWidth = road.clientWidth / 2
    const bushes = document.querySelectorAll('.bush')
    const mountains = document.querySelectorAll('.mountain')
    const sprites = [...bushes, ...mountains]
    const spriteCoords = []

    for (let i = 0; i < sprites.length; i++) {
        const sprite = sprites[i]
        const spriteCoord = getCoords(sprite)
        spriteCoords.push(spriteCoord)
    }
    document.addEventListener('keydown', (event) => {
        if (isPause) {
            return
        }
        const code = event.code
        if ((code === 'ArrowUp' || code === 'KeyW') && carInfo.move.top === null) {
            if (carInfo.move.down) {
                return
            }
            carInfo.move.top = requestAnimationFrame(carMoveToTop)
        } else if ((code === 'ArrowDown' || code === 'KeyS') && carInfo.move.bottom === null) {
            if (carInfo.move.top) {
                return
            }
            carInfo.move.bottom = requestAnimationFrame(carMoveToBottom)
        } else if ((code === 'ArrowLeft' || code === 'KeyA') && carInfo.move.left === null) {
            if (carInfo.move.right) {
                return
            }
            carInfo.move.left = requestAnimationFrame(carMoveToLeft)
        } else if ((code === 'ArrowRight' || code === 'KeyD') && carInfo.move.right === null) {
            if (carInfo.move.left) {
                return
            }
            carInfo.move.right = requestAnimationFrame(carMoveToRight)
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

    function carMoveToTop() {
        const newY = carInfo.coords.y - 5
        if (newY < 0) {
            return
        }
        carInfo.coords.y = newY
        setCarCoords(carInfo.coords.x, newY)
        carInfo.move.top = requestAnimationFrame(carMoveToTop)
    }


    function carMoveToBottom() {
        const newY = carInfo.coords.y + 5
        if (newY + carInfo.height > roadHeight) {
            return
        }
        carInfo.coords.y = newY
        setCarCoords(carInfo.coords.x, newY)
        carInfo.move.bottom = requestAnimationFrame(carMoveToBottom)
    }

    function carMoveToRight() {
        const newX = carInfo.coords.x + 5
        if (newX > roadWidth - carInfo.width) {
            return
        }
        carInfo.coords.x = newX
        setCarCoords(newX, carInfo.coords.y)
        carInfo.move.right = requestAnimationFrame(carMoveToRight)
    }

    function carMoveToLeft() {
        const newX = carInfo.coords.x - 5
        if (newX  < -roadWidth + carInfo.width) {
            return
        }
        carInfo.coords.x = newX
        setCarCoords(newX, carInfo.coords.y)
        carInfo.move.left = requestAnimationFrame(carMoveToLeft)
    }

    function setCarCoords(x, y) {
        car.style.transform = `translate(${x}px, ${y}px)`
    }

    animationId = requestAnimationFrame(startGame)

    function startGame() {
        elementAnimation(danger, dangerInfo, -250)
        if (dangerInfo.visible && hasCollision(carInfo, dangerInfo)) {
            return finishGame()

        }
        spritesAnimation()
        elementAnimation(coin, coinInfo, -100)
        if (coinInfo.visible && hasCollision(carInfo, coinInfo)) {
            score += 1
            gameScore.innerText = score
            coin.style.display = 'none'
            coinInfo.visible = false
            if (score % 5 === 0) {
                speed += 1
            }

        }


        //elementAnimation(arrow, arrowInfo,  -600)
        animationId = requestAnimationFrame(startGame)
    }

    function spritesAnimation() {
        for (let i = 0; i < sprites.length; i++) {
            const sprite = sprites[i]
            const coords = spriteCoords[i]
            let newY = coords.y + speed

            if (newY > window.innerHeight) {
                newY = -700
            }
            spriteCoords[i].y = newY
            sprite.style.transform = `translate(${coords.x}px, ${newY}px)`

        }

    }

    function elementAnimation(elem, elemInfo, elemInitialYCoord) {
        let newY = elemInfo.coords.y + speed
        let newX = elemInfo.coords.x
        if (newY > window.innerHeight) {
            newY = elemInitialYCoord
            const direction = parseInt(Math.random() * 2)
            const randomXCoord = parseInt(Math.random() * (roadWidth + 1 - elemInfo.width))
            newX = direction === 0 ? -randomXCoord : randomXCoord
            elem.style.display = 'initial'
            elemInfo.visible = true
        }
        elemInfo.coords.y = newY
        elemInfo.coords.x = newX
        elem.style.transform = `translate(${newX}px, ${newY}px)`
    }

    function getCoords(element) {
        const matrix = window.getComputedStyle(element).transform
        const array = matrix.split(',')
        const y = array[array.length - 1]
        const x = array[array.length - 2]
        return {x: parseFloat(x), y: parseFloat(y)}
    }

    function hasCollision(elem1Info, elem2Info) {
        const carYTop = elem1Info.coords.y
        const carYBottom = elem1Info.coords.y + elem1Info.height
        const coinYTop = elem2Info.coords.y
        const coinYBottom = elem2Info.coords.y + elem2Info.height
        const carXLeft = elem1Info.coords.x - elem1Info.width
        const carXRight = elem1Info.coords.x + elem1Info.width
        const coinXLeft = elem2Info.coords.x - elem2Info.width
        const coinXRight = elem2Info.coords.x + elem2Info.width
        if (carYTop > coinYBottom || carYBottom < coinYTop) {
            console.log('car', carInfo.coords)
            console.log('danger', dangerInfo.coords)
            return false
        }
        if (carXLeft > coinXRight || carXRight < coinXLeft) {
            return false
        }

        return true
    }

    function cancelAnimations() {
        cancelAnimationFrame(animationId)
        cancelAnimationFrame(carInfo.move.top)
        cancelAnimationFrame(carInfo.move.bottom)
        cancelAnimationFrame(carInfo.move.left)
        cancelAnimationFrame(carInfo.move.right)
    }
    function finishGame() {
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
