
class Overlay {
    constructor() { }
    static show() {
        $("#overlay").css("display", "flex");
    }
    static hide() {
        $("#overlay").css("display", "none");
    };
    static async text(s) {
        $("#overlaytext").text(s);
    };
}
export { Overlay as overlay };