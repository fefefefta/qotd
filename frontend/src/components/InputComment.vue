<template>
  <div class="flex flex-col mt-4">
    <textarea
      class="textarea textarea-bordered w-full shadow-md"
      :placeholder="placeholderText"
      v-model="localText"
    ></textarea>
    <button class="btn btn-primary btn-sm mt-2 self-end" @click="submit">Submit</button>
  </div>
</template>

<script>
import apiClient from '../api';

export default {
  name: 'InputComment',
  props: {
    text: {
      type: String,
      default: ""
    },
    placeholderText: {
      type: String,
      default: "What do you think?"
    },
    parentCommentId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      localText: this.text // используем локальную копию текста для двусторонней привязки
    };
  },
  watch: {
    text(newText) {
      this.localText = newText;
    },
    localText(newText) {
      this.$emit('update:text', newText);
    }
  },
  methods: {
    submit() {
      this.$emit('submit', this.localText);
      this.localText = null;
    },
  }
};
</script>
