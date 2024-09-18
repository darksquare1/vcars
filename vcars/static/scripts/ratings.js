const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const csrftoken = getCookie("csrftoken");

const ratingButtons = document.querySelectorAll('.rating-buttons');

ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        const value = parseInt(event.target.dataset.value)
        const picId = parseInt(event.target.dataset.pic)
        const ratingSum = button.querySelector('.rating-sum');
        const formData = new FormData();
        formData.append('pic_id', picId);
        formData.append('value', value);
        fetch("/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.error(error));
    });
});
