<template>
  <div>
    <div class="flex justify-end">
      <div v-if="comments.length" class="relative">
        <button @click="isOpen = !isOpen" class="btn btn-primary btn-sm">Сортировать</button>
        <ul
          v-show="isOpen"
          @click.away="isOpen = false"
          class="absolute mt-2 py-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg"
        >
          <li><button @click="sortByOldest" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Старые сначала</button></li>
          <li><button @click="sortByNewest" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Новые сначала</button></li>
          <li><button @click="sortByPopular" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Популярные сначала</button></li>
        </ul>
      </div>
    </div>
    <Comment v-for="comment in sortedComments" :key="comment.id" :comment="comment" />
    <InputComment class="" @submit="handleCommentSubmit"/>
  </div>
</template>

<script>
import axios from '../api.js';
import { getCookie } from '../utils/cookies';
import eventBus from '../utils/eventBus.js';

import Comment from './Comment.vue'
import InputComment from './InputComment.vue';

export default {
  name: 'CommentSection',
  components: {
    Comment,
    InputComment,
  },
  props: {
    comments: {
      type: Array,
      required: true
    },
    question_id: {
      type: Number,
      required: false
    }
  },
  data() {
    return {
      commentsArray: [],
      sortBy: 'popular', // текущий тип сортировки
      isOpen: false,
    }
  },
  computed: {
    sortedComments() {
      if (!this.sortBy) {
        return this.commentsArray;
      }

      // Создаем копию массива комментариев для сортировки
      let sorted = [...this.commentsArray];

      // Выполняем сортировку в зависимости от выбранного типа
      if (this.sortBy === 'oldest') {
        sorted.sort((a, b) => a.id - b.id); // по возрастанию comment.id
      } else if (this.sortBy === 'newest') {
        sorted.sort((a, b) => b.id - a.id); // по убыванию comment.id
      } else if (this.sortBy === 'popular') {
        sorted.sort((a, b) => b.upvotes - a.upvotes); // по убыванию comment.upvotes
      }

      return sorted;
    }
  },
  methods: {
    async handleCommentSubmit(text) {
      try {
        const response = await axios.post('/comment/', {
          text: text,
          question_id: this.question_id
        });
        const newComment = response.data;
        this.commentsArray.push(newComment);
        if (response.data.is_new_user) {
          eventBus.emit('newUserCreated', response.data.username);
        }
        console.log('Comment submitted successfully:', response.data);
      } catch (error) {
        console.error('Error submitting comment:', error);
      }
    },
    sortByOldest() {
      this.sortBy = 'oldest';
    },
    sortByNewest() {
      this.sortBy = 'newest';
    },
    sortByPopular() {
      this.sortBy = 'popular';
    }
  },
  mounted() {
    // Инициализация массива комментариев при загрузке компонента
    this.commentsArray = this.comments;
  },
  watch: {
    comments(newVal) {
      // Обновление массива комментариев при изменении входящих данных
      this.commentsArray = newVal;
    }
  }
}
</script>

<style scoped>
</style>
