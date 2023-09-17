async function setColors(page) {
    if (!instructionBlocks[page - 1].childNodes.length) {

        // Здесь должен запрашиваться массив цветов в формате JSON

        // let url = `https://example_url/${page - 1}`;
        // let response = await fetch(url);

        // let colors = await response.json();

        for (let i = 0; i < 160; i++) {
            let colorSpan = document.createElement('span');
            colorSpan.className = "square";

            // Здесь должны получаться числа из массива и подставляться цвета 

            // let c = colors[i];
            // colorSpan.style.backgroundColor = `rgb(${c[0]}, ${c[1]}, ${c[2]})`;

            let c = Math.random() * 255;
            colorSpan.style.backgroundColor = `rgb(${c}, ${c}, ${c})`;

            // Верхние 2 строчки убрать, когда заработают запросы (это просто рандомные оттенки серого для теста)

            colorSpan.style.border = "solid 2px black"
            instructionBlocks[page - 1].append(colorSpan);
        }
    }
}

function setPage(page) {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set('page', page);
    const newRelativePathQuery =
        window.location.pathname + '?' + searchParams.toString();
    history.pushState(null, '', newRelativePathQuery);

    setColors(page);
}

function pagination(event) {
    var e = event || window.event;
    var target = e.target;
    var id = target.id;

    if (target.tagName.toLowerCase() != "span") return;

    var data_page = +target.dataset.page;
    main_page.classList.remove("paginator_active");
    main_page = document.getElementById(id);
    main_page.classList.add("paginator_active");

    var j = 0;
    for (var i = 0; i < div_block.length; i++) {
        var data_num = div_block[i].dataset.num;
        if (data_num <= data_page || data_num >= data_page)
            div_block[i].style.display = "none";

    }
    for (var i = data_page; i < div_block.length; i++) {
        if (j >= cnt) break;
        div_block[i].style.display = "block";
        j++;

        setPage(i + 1);
    }
}

const instructionBlocks = Array.from(document.getElementsByClassName('colors-block'));

setPage(1);

var count = 120;
var cnt = 1;
var cnt_page = Math.ceil(count / cnt);

var paginator = document.querySelector(".paginator");
var page = "";
for (var i = 0; i < cnt_page; i++) {
    page += "<span data-page=" + i * cnt + "  id=\"page" + (i + 1) + "\">" + (i + 1) + "</span>";
}
paginator.innerHTML = page;

var div_block = document.querySelectorAll(".instruction-block");
for (var i = 0; i < div_block.length; i++) {
    if (i < cnt) {
        div_block[i].style.display = "block";
    }
}

var main_page = document.getElementById("page1");
main_page.classList.add("paginator_active");