function handleSearch(event){
    event.preventDefault()
    let input = document.getElementById('search-input').value
    if (input){
        document.location.href = '/?query=' + input
    }
}
const searchForm = document.getElementById('search-form')
searchForm.addEventListener('submit', handleSearch)