function add_new(){
    document.getElementById("new").style.display = "inline";
    document.getElementById("add").style.display = "none";
    document.getElementById("rem").style.display = "flex";
};
function add_rem(){
    document.getElementById("new").style.display = "none";
    document.getElementById("add").style.display = "flex";
    document.getElementById("rem").style.display = "none";
};
function show(id){
    document.getElementById("hide" + id).style.display = "inline";
};
function hide(id){
    document.getElementById("hide" + id).style.display = "none";
};
const faq = document.getElementById("course_faq");
console.log(faq);
if (faq !== null) {
    faq.onclick = (e) => {
        e.preventDefault();
        const f = document.getElementById("faq_end");
        f.scrollIntoView({ behavior: "smooth" });
    }
}