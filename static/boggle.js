class BoggleGame {
    constructor(boardId, secs = 60) {
        this.secs = secs
        this.showTimer();
        this.board = $('#' + boardId)
        this.score = 0;
        this.word = new Set();

        this.timer = setInterval(this.tick.bind(this), 1000)

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
    showWord(word) {
        $(".word", this.board).append($("<li>", { text: word }));
    }
    showScore() {
        $(".score", this.board).text(this.score);
    }
    showMessage(msg, cls) {
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.word.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return
        }

        const resp = await axios.get("/check-word", { params: { word: word }});
        if (resp.data.result === "not-word") {
            this.showMessage(`${word} is not a vaild English word`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a word on this board`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.word.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }
        $word.val("").focus();
    }

    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/submit-score", { score: this.score });
        if (resp.data.topScore) {
            this.showMessage(`New score: ${this.score}`, "ok");
        } else {
            this.showMessage(`End score: ${this.score}`, "ok");
        }
    }
}