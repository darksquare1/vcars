function createElementInfo(element) {
    return {
        width: element.clientWidth / 2,
        height: element.clientHeight,
        coords: getCoords(element),
        visible: true,
        ignoreAppearance: false,

    }
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
        return false
    }
    if (carXLeft > coinXRight || carXRight < coinXLeft) {
        return false
    }

    return true
}