export const state = () => ({
  ME: {
    accessToken:"Bearer fdsajfdksalionhu"
  }
});

export const mutations = {
  add (state, text) {
    state.list.push({
      text,
      done: false,
      id: Date.now()
    })
  },
  remove (state, todo) {
    state.list = state.list.filter(item => item.id !== todo.id)
  },
  toggle (state, todo) {
    todo.done = !todo.done
  },
  addtolist(state,list){
    state.list=list
  }
};
