function elementAnimation(elem, elemInfo, speed, elemInitialYCoord) {
    let newY = elemInfo.coords.y + speed
    let newX = elemInfo.coords.x
    if (newY > window.innerHeight) {
        newY = elemInitialYCoord
        const direction = parseInt(Math.random() * 2)
        const randomXCoord = parseInt(Math.random() * (roadWidth + 1 - elemInfo.width))
        newX = direction === 0 ? -randomXCoord : randomXCoord
        if (!elemInfo.ignoreAppearance) {
            elem.style.display = 'initial'
            elemInfo.visible = true
        }
    }
    elemInfo.coords.y = newY
    elemInfo.coords.x = newX
    elem.style.transform = `translate(${newX}px, ${newY}px)`
}