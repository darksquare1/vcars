const bushes = document.querySelectorAll('.bush')
const mountains = document.querySelectorAll('.mountain')
const sprites = [...bushes, ...mountains]
const spriteCoords = []
for (let i = 0; i < sprites.length; i++) {
    const sprite = sprites[i]
    const spriteCoord = getCoords(sprite)
    spriteCoords.push(spriteCoord)
}

function spritesAnimation(speed) {
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