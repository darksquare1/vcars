function carMoveToTop(car, carInfo) {
    return () => {
        const newY = carInfo.coords.y - 5
        if (newY < 0) {
            return
        }
        carInfo.coords.y = newY
        setCarCoords(car, carInfo.coords.x, newY)
        carInfo.move.top = requestAnimationFrame(carMoveToTop(car, carInfo))
    }

}

function carMoveToBottom(car, carInfo) {
    return () => {
        const newY = carInfo.coords.y + 5
        if (newY + carInfo.height > roadHeight) {
            return
        }
        carInfo.coords.y = newY
        setCarCoords(car, carInfo.coords.x, newY)
        carInfo.move.bottom = requestAnimationFrame(carMoveToBottom(car, carInfo))
    }

}

function carMoveToRight(car, carInfo) {
    return () => {
        const newX = carInfo.coords.x + 5
        if (newX > roadWidth - carInfo.width) {
            return
        }
        carInfo.coords.x = newX
        setCarCoords(car, newX, carInfo.coords.y)
        carInfo.move.right = requestAnimationFrame(carMoveToRight(car, carInfo))
    }

}

function carMoveToLeft(car, carInfo) {
    return () => {
        const newX = carInfo.coords.x - 5
        if (newX < -roadWidth + carInfo.width) {
            return
        }
        carInfo.coords.x = newX
        setCarCoords(car, newX, carInfo.coords.y)
        carInfo.move.left = requestAnimationFrame(carMoveToLeft(car, carInfo))
    }

}

function setCarCoords(car, x, y) {
    car.style.transform = `translate(${x}px, ${y}px)`
}