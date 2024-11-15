(function () {
    let isPause = false
    let animationId = null

    const speed = 3

    const car = document.querySelector('.car')
    const bushes = document.querySelectorAll('.bush')
    const mountains = document.querySelectorAll('.mountain')
    const sprites = [...bushes, ...mountains]
    const spriteCoords = []
    for (let i = 0; i < sprites.length; i++) {
        const sprite = sprites[i]
        const spriteCoord = getCoords(sprite)
        spriteCoords.push(spriteCoord)
    }
    animationId = requestAnimationFrame(startGame)

    function startGame() {
        spritesAnimation()
        animationId = requestAnimationFrame(startGame)
    }

    function spritesAnimation() {
        for (let i = 0; i < sprites.length; i++){
            const sprite = sprites[i]
            const coords = spriteCoords[i]
            let newY = coords.y + speed

            if (newY > window.innerHeight){
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
            cancelAnimationFrame(animationId);
            gameButton.children[0].style.display = 'none'
            gameButton.children[1].style.display = 'initial'
        } else {
            aminationId = requestAnimationFrame(startGame)
            gameButton.children[0].style.display = 'initial'
            gameButton.children[1].style.display = 'none'
        }
    })
})()