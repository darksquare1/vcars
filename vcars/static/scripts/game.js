(function () {
    let isPause = false
    let animationId = null

    const speed = 3

    const car = document.querySelector('.car')
    const bushes = document.querySelectorAll('.bush')
    const mountains = document.querySelectorAll('.mountain')
    const bush1 = bushes[0]
    const coordsBush1 = getCoords(bush1)

    animationId = requestAnimationFrame(startGame)

    function startGame() {
        spritesAnimation()
        animationId = requestAnimationFrame(startGame)
    }

    function spritesAnimation() {
        const newY = coordsBush1.y + speed
        coordsBush1.y = newY
        bush1.style.transform = `translate(${coordsBush1.x}px, ${newY}px)`
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