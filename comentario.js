const store = new Vuex.Store({
    state: {
      comments: [
        { username: 'Juan Pérez', message: 'Excelente producto, muy recomendado.', rating: 5, date: '2024-11-15' },
        { username: 'Ana García', message: 'Buen servicio, pero llegó tarde.', rating: 3, date: '2024-11-14' },
      ]
    },
    mutations: {
      addComment(state, comment) {
        state.comments.push(comment);
      }
    }
  });

  new Vue({
    el: '#app',
    store,
    data: {
      newComment: {
        username: '',
        message: '',
        rating: 5
      }
    },
    computed: {
      comments() {
        return this.$store.state.comments;
      }
    },
    methods: {
      submitComment() {
        const newComment = { 
          ...this.newComment, 
          date: new Date().toLocaleDateString() 
        };
        this.$store.commit('addComment', newComment);
        this.newComment.username = '';
        this.newComment.message = '';
        this.newComment.rating = 5;
      }
    }
  });