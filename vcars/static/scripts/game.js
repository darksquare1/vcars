(function () {
    let isPause = false
    let animationId = null
    const speed = 3
    const car = document.querySelector('.car')
    const carWidth = car.clientWidth
    const carHeight = car.clientHeight
    const road = document.querySelector('.road')
    const roadHeight = road.clientHeight
    const roadWidth = road.clientWidth
    const bushes = document.querySelectorAll('.bush')
    const mountains = document.querySelectorAll('.mountain')
    const sprites = [...bushes, ...mountains]
    const spriteCoords = []
    const carCoords = getCoords(car)
    const carMove = {
        top: null,
        bottom: null,
        left: null,
        right: null,
    }
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
        if ((code === 'ArrowUp' || code === 'KeyW') && carMove.top === null) {
            if (carMove.down) {
                return
            }
            carMove.top = requestAnimationFrame(carMoveToTop)
        } else if ((code === 'ArrowDown' || code === 'KeyS') && carMove.bottom === null) {
            if (carMove.top) {
                return
            }
            carMove.bottom = requestAnimationFrame(carMoveToBottom)
        } else if ((code === 'ArrowLeft' || code === 'KeyA') && carMove.left === null) {
            if (carMove.right) {
                return
            }
            carMove.left = requestAnimationFrame(carMoveToLeft)
        } else if ((code === 'ArrowRight' || code === 'KeyD') && carMove.right === null) {
            if (carMove.left) {
                return
            }
            carMove.right = requestAnimationFrame(carMoveToRight)
        }

    })
    document.addEventListener('keyup', (event) => {
        const code = event.code
        if (code === 'ArrowUp' || code === 'KeyW') {
            cancelAnimationFrame(carMove.top)
            carMove.top = null
        } else if (code === 'ArrowDown' || code === 'KeyS') {
            cancelAnimationFrame(carMove.bottom)
            carMove.bottom = null

        } else if (code === 'ArrowLeft' || code === 'KeyA') {
            cancelAnimationFrame(carMove.left)
            carMove.left = null
        } else if (code === 'ArrowRight' || code === 'KeyD') {
            cancelAnimationFrame(carMove.right)
            carMove.right = null
        }

    })

    function carMoveToTop() {
        const newY = carCoords.y - 5
        if (newY < 0) {
            return
        }
        carCoords.y = newY
        setCarCoords(carCoords.x, newY)
        carMove.top = requestAnimationFrame(carMoveToTop)
    }

    function carMoveToBottom() {
        const newY = carCoords.y + 5
        if (newY + carHeight > roadHeight) {
            return
        }
        carCoords.y = newY
        setCarCoords(carCoords.x, newY)
        carMove.bottom = requestAnimationFrame(carMoveToBottom)
    }

    function carMoveToRight() {
        const newX = carCoords.x + 5
        if (newX + 50 > roadWidth - carWidth) {
            return
        }
        carCoords.x = newX
        setCarCoords(newX, carCoords.y)
        carMove.right = requestAnimationFrame(carMoveToRight)
    }

    function carMoveToLeft() {
        const newX = carCoords.x - 5
        if (newX - 50 < -roadWidth + carWidth) {
            return
        }
        carCoords.x = newX
        setCarCoords(newX, carCoords.y)
        carMove.left = requestAnimationFrame(carMoveToLeft)
    }

    function setCarCoords(x, y) {
        car.style.transform = `translate(${x}px, ${y}px)`
    }

    animationId = requestAnimationFrame(startGame)

    function startGame() {
        spritesAnimation()
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


    function getCoords(element) {
        const matrix = window.getComputedStyle(element).transform
        const array = matrix.split(',')
        const y = array[array.length - 1]
        const x = array[array.length - 2]
        return {x: parseFloat(x), y: parseFloat(y)}
    }

    const gameButton = document.querySelector('.game-button')
    gameButton.addEventListener('click', () => {
        isPause = !isPause;
        if (isPause) {
            cancelAnimationFrame(animationId)
            cancelAnimationFrame(carMove.top)
            cancelAnimationFrame(carMove.bottom)
            cancelAnimationFrame(carMove.left)
            cancelAnimationFrame(carMove.right)
            gameButton.children[0].style.display = 'none'
            gameButton.children[1].style.display = 'initial'
        } else {
            aminationId = requestAnimationFrame(startGame)
            gameButton.children[0].style.display = 'initial'
            gameButton.children[1].style.display = 'none'
        }
    })
})()