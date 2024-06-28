<template>
  <div class="p-4 mb-1 w-full">
    <div class='flex items-center justify-between mb-2'>
      <div class="flex items-center">
        <img :src="`https://robohash.org/${comment.username}.png`" alt="Avatar" class="w-8 h-8 rounded-full mr-2">
        <strong :class="{
          'text-gray-800': true,
          'bg-yellow-200': comment.username === currentUserUsername,
        }">{{ comment.username }}</strong>
      </div>
    </div>
    <p class="text-gray-700 text-left">{{ comment.text }}</p>
    <div class="flex justify-start mt-2">
      <button
        :class="{
          'badge badge-primary text-gray-600': true,
          'badge-outline': !comment.voted
        }"
        @click="vote">
        {{ comment.upvotes }} votes
      </button>
      <small class="underline cursor-pointer ml-2" @click="reply">reply</small>
    </div>
    <div class="pl-4 border-l-1 border-gray-300">
      <InputComment :text="'@' + comment.username + ', '" v-if="replyIsClicked" @reply="reply" @submit="handleCommentSubmit" />
      <div class="mt-2">
        <Comment v-for="child in comment.children" :key="child.id" :comment="child" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../api.js';
import { getCookie, setCookie, removeCookie } from '../utils/cookies';
import eventBus from '../utils/eventBus.js';

import InputComment from './InputComment.vue';

export default {
  name: 'Comment',
  props: {
    comment: {
      type: Object,
      required: true
    }
  },
  components: {
    InputComment,
  },
  data() {
    return {
      replyIsClicked: false,
    }
  },
  computed: {
    currentUserUsername() {
      return getCookie('current_user')?.username
    }
  },
  methods: {
    reply() {
      this.replyIsClicked = !this.replyIsClicked
    },

    async vote() {
      const currentUserExists = !!getCookie('current_user')?.username;

      try {
        const response = await apiClient.post('/votes/', {
          comment_id: this.comment.id
        });
      } catch (error) {
        console.error('Error submitting vote:', error);
      }
      if (!this.comment.voted) {
          this.comment.upvotes += 1;
          this.comment.voted = true;
        } else {
          this.comment.upvotes -= 1;
          this.comment.voted = false;
        };

      if (!currentUserExists && getCookie('current_user')) {
        eventBus.emit('newUserCreated', getCookie('current_user').username);
      }
    },

    async handleCommentSubmit(text) {
      const currentUserExists = !!getCookie('current_user');

      try {
        const response = await apiClient.post('/comment/', {
          text: text,
          parent_id: this.comment.id,
          question_id: this.comment.question_id
        });
        const newComment = response.data;
        console.log(newComment);
        this.comment.children.push(newComment);
        this.reply();
        console.log('Comment submitted successfully:', response.data);
      } catch (error) {
        console.error('Error submitting comment:', error);
      }

      if (!currentUserExists && getCookie('current_user')) {
        eventBus.emit('newUserCreated', getCookie('current_user').username);
      }
    },
  }
}
</script>

<style scoped>
.border-l-1 {
  border-left-width: 1px;
}
</style>