  
 


document.getElementById("search").addEventListener("input", filterLogs);
document.getElementById("filter").addEventListener("change", filterLogs);

function filterLogs() {
    let searchValue = document.getElementById("search").value.toLowerCase();
    let filterValue = document.getElementById("filter").value;
    
    document.querySelectorAll("tbody tr").forEach(row => {
        let ip = row.children[1].innerText.toLowerCase();
        let decision = row.children[2].innerText.toLowerCase();

        let matchesSearch = ip.includes(searchValue);
        let matchesFilter = filterValue === "all" || decision === filterValue;

        row.style.display = matchesSearch && matchesFilter ? "" : "none";
    });
}