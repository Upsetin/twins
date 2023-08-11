<link rel="stylesheet" href="./assets/index.css">
<template>
    <div id="app">
        <div id="app-nex">
            <div id="fir" class="app-fir">
                <div class="app-fir-one md:pl-[260px]">

                    <div
                        class="sticky top-0 z-10 flex items-center border-b border-white/20 bg-gray-800 pl-1 pt-1 text-gray-200 sm:pl-3 md:hidden     box-shadow: rgba(2, 2, 2, 0.3) 1px 2px 4px"
                        style="border-radius: 0px 0px 3px 3px">
                        <div>
                            <button @click="showSlideMethod" type="button"
                                    class="show-buttonhover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white dark:hover:text-white">
                <span class="daohang-only">
                  打开导航栏
                </span>
                                <svg stroke="currentColor" fill="none" stroke-width="1.5" viewBox="0 0 24 24"
                                     stroke-linecap="round"
                                     stroke-linejoin="round" class="svg" height="1em" width="1em"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <line x1="3" y1="12" x2="21" y2="12"></line>
                                    <line x1="3" y1="6" x2="21" y2="6"></line>
                                    <line x1="3" y1="18" x2="21" y2="18"></line>
                                </svg>
                            </button>
                        </div>
                        <h1 class="h-1">{{ chatTitle }}</h1>
                        <button @click.stop="newChat" type="button" class="px-3">
                            <svg stroke="currentColor" fill="none" stroke-width="1.5" viewBox="0 0 24 24"
                                 stroke-linecap="round"
                                 stroke-linejoin="round" class="svg" height="1em" width="1em"
                                 xmlns="http://www.w3.org/2000/svg">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                        </button>
                    </div>

                    <main class="maincon">
                        <!--主要的对话内容            -->
                        <div class="maincon-div">
                            <div class="react-scroll-to-bottom--css-ncqif-79elbk height-full dark:bg-gray-800">
                                <div ref="chatContainer" @click="closeShowSlide"
                                     class="react-scroll-to-bottom--css-krija-1n7m0yu">
                                    <div class="maincon-div2 dark:bg-gray-800">
                                        <template v-for="(conv, idx) in conversation">
                                            <div v-if="conv.speaker === 'user'"
                                                 class="width-full border-b border-black/10 dark:border-gray-900/50 text-gray-700 dark:text-gray-100 group dark:bg-gray-800">
                                                <div
                                                    class="text-base gap-4 md:gap-6 m-auto md:max-w-2xl lg:max-w-2xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0">
                                                    <div class="w-[30px] flex flex-col relative items-end">
                                                        <div class="relative flex">
                              <span
                                  style="box-sizing: border-box; display: inline-block; overflow: hidden; width: initial; height: initial; background: none; opacity: 1; border: 0px; margin: 0px; padding: 0px; position: relative; max-width: 100%;">
                                <span
                                    style="box-sizing: border-box; display: block; width: initial; height: initial; background: none; opacity: 1; border: 0px; margin: 0px; padding: 0px; max-width: 100%;">
                                  <img aria-hidden="true" :src="pic"
                                       style="display: block; max-width: 100%; width: initial; height: initial; background: none; opacity: 1; border: 0px; margin: 0px; padding: 0px;">
                                </span>
                              </span>
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="relative flex w-[calc(100%-50px)] flex-col gap-1 md:gap-3 lg:w-[calc(100%-115px)]">
                                                        <div class="flex flex-grow flex-col gap-3">
                                                            <div id="speechmsg"
                                                                 class="min-h-[20px] flex flex-col items-start gap-4 whitespace-pre-wrap">
                                                                {{ conv.speech }}
                                                            </div>
                                                        </div>
                                                        <div v-if="false"
                                                             class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible">
                                                            <button
                                                                class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400 md:invisible md:group-hover:visible">
                                                                <svg stroke="currentColor" fill="none" stroke-width="2"
                                                                     viewBox="0 0 24 24"
                                                                     stroke-linecap="round" stroke-linejoin="round"
                                                                     class="newchater" height="1em"
                                                                     width="1em"
                                                                     xmlns="http://www.w3.org/2000/svg">
                                                                    <path
                                                                        d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                                                    <path
                                                                        d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                                                                </svg>
                                                            </button>
                                                        </div>
                                                        <div class="flex justify-between"></div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="conv.speaker === 'assitant'"
                                                 class="width-full border-b border-black/10 dark:border-gray-900/50 text-gray-700 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]">
                                                <div
                                                    class="font-color text-base gap-4 md:gap-6 m-auto md:max-w-2xl dark:bg-[#444654] lg:max-w-2xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0">
                                                    <!--                                                    <div class="w-[30px] flex flex-col relative items-end">-->
                                                    <!--                                                        <div-->
                                                    <!--                                                            class="relative h-[30px] w-[30px] p-1 rounded-sm text-white flex items-center justify-center"-->
                                                    <!--                                                            style="background-color: #2a2b32">-->
                                                    <!--                                                            <font-awesome-icon :icon="['fa', 'fa-bug']"/>-->
                                                    <!--                                                        </div>-->
                                                    <!--                                                        &lt;!&ndash; 多个消息 &ndash;&gt;-->
                                                    <!--                                                        <div v-if="conv.speeches.length > 0"-->
                                                    <!--                                                             class="text-xs flex items-center justify-center gap-1 invisible absolute left-0 top-2 -ml-4 -translate-x-full group-hover:visible">-->
                                                    <!--                                                            <button @click.stop="last(conv)" :disabled="!(conv.idx > 0)"-->
                                                    <!--                                                                    class="dark:text-white disabled:text-gray-300 dark:disabled:text-gray-400">-->
                                                    <!--                                                                <svg stroke="currentColor" fill="none"-->
                                                    <!--                                                                     stroke-width="1.5" viewBox="0 0 24 24"-->
                                                    <!--                                                                     stroke-linecap="round" stroke-linejoin="round"-->
                                                    <!--                                                                     class="newchater-3" height="1em"-->
                                                    <!--                                                                     width="1em"-->
                                                    <!--                                                                     xmlns="http://www.w3.org/2000/svg">-->
                                                    <!--                                                                    <polyline points="15 18 9 12 15 6"></polyline>-->
                                                    <!--                                                                </svg>-->
                                                    <!--                                                            </button>-->
                                                    <!--                                                            <span class="flex-grow flex-shrink-0">{{ conv.idx + 1 }} / {{-->
                                                    <!--                                                                    conv.speeches.length-->
                                                    <!--                                                                }}</span>-->
                                                    <!--                                                            <button style="margin-right: 1rem" @click.stop="next(conv)"-->
                                                    <!--                                                                    :disabled="!(conv.idx < conv.speeches.length - 1)"-->
                                                    <!--                                                                    class="dark:text-white disabled:text-gray-300 dark:disabled:text-gray-400">-->
                                                    <!--                                                                <svg stroke="currentColor" fill="none"-->
                                                    <!--                                                                     stroke-width="1.5" viewBox="0 0 24 24"-->
                                                    <!--                                                                     stroke-linecap="round" stroke-linejoin="round"-->
                                                    <!--                                                                     class="newchater-3" height="1em"-->
                                                    <!--                                                                     width="1em"-->
                                                    <!--                                                                     xmlns="http://www.w3.org/2000/svg">-->
                                                    <!--                                                                    <polyline points="9 18 15 12 9 6"></polyline>-->
                                                    <!--                                                                </svg>-->
                                                    <!--                                                            </button>-->
                                                    <!--                                                        </div>-->
                                                    <!--                                                    </div>-->
                                                    <div class="w-[30px]">
                                                        <div
                                                            class="relative p-1 rounded-sm h-[30px] w-[30px] text-white flex items-center justify-center"
                                                            style="background-color: rgb(25, 195, 125);">
                                                            <svg width="41" height="41" viewBox="0 0 41 41" fill="none"
                                                                 xmlns="http://www.w3.org/2000/svg" stroke-width="1.5"
                                                                 role="img"><title>ChatGPT</title>
                                                                <text x="-9999" y="-9999">ChatGPT</text>
                                                                <path
                                                                    d="M37.5324 16.8707C37.9808 15.5241 38.1363 14.0974 37.9886 12.6859C37.8409 11.2744 37.3934 9.91076 36.676 8.68622C35.6126 6.83404 33.9882 5.3676 32.0373 4.4985C30.0864 3.62941 27.9098 3.40259 25.8215 3.85078C24.8796 2.7893 23.7219 1.94125 22.4257 1.36341C21.1295 0.785575 19.7249 0.491269 18.3058 0.500197C16.1708 0.495044 14.0893 1.16803 12.3614 2.42214C10.6335 3.67624 9.34853 5.44666 8.6917 7.47815C7.30085 7.76286 5.98686 8.3414 4.8377 9.17505C3.68854 10.0087 2.73073 11.0782 2.02839 12.312C0.956464 14.1591 0.498905 16.2988 0.721698 18.4228C0.944492 20.5467 1.83612 22.5449 3.268 24.1293C2.81966 25.4759 2.66413 26.9026 2.81182 28.3141C2.95951 29.7256 3.40701 31.0892 4.12437 32.3138C5.18791 34.1659 6.8123 35.6322 8.76321 36.5013C10.7141 37.3704 12.8907 37.5973 14.9789 37.1492C15.9208 38.2107 17.0786 39.0587 18.3747 39.6366C19.6709 40.2144 21.0755 40.5087 22.4946 40.4998C24.6307 40.5054 26.7133 39.8321 28.4418 38.5772C30.1704 37.3223 31.4556 35.5506 32.1119 33.5179C33.5027 33.2332 34.8167 32.6547 35.9659 31.821C37.115 30.9874 38.0728 29.9178 38.7752 28.684C39.8458 26.8371 40.3023 24.6979 40.0789 22.5748C39.8556 20.4517 38.9639 18.4544 37.5324 16.8707ZM22.4978 37.8849C20.7443 37.8874 19.0459 37.2733 17.6994 36.1501C17.7601 36.117 17.8666 36.0586 17.936 36.0161L25.9004 31.4156C26.1003 31.3019 26.2663 31.137 26.3813 30.9378C26.4964 30.7386 26.5563 30.5124 26.5549 30.2825V19.0542L29.9213 20.998C29.9389 21.0068 29.9541 21.0198 29.9656 21.0359C29.977 21.052 29.9842 21.0707 29.9867 21.0902V30.3889C29.9842 32.375 29.1946 34.2791 27.7909 35.6841C26.3872 37.0892 24.4838 37.8806 22.4978 37.8849ZM6.39227 31.0064C5.51397 29.4888 5.19742 27.7107 5.49804 25.9832C5.55718 26.0187 5.66048 26.0818 5.73461 26.1244L13.699 30.7248C13.8975 30.8408 14.1233 30.902 14.3532 30.902C14.583 30.902 14.8088 30.8408 15.0073 30.7248L24.731 25.1103V28.9979C24.7321 29.0177 24.7283 29.0376 24.7199 29.0556C24.7115 29.0736 24.6988 29.0893 24.6829 29.1012L16.6317 33.7497C14.9096 34.7416 12.8643 35.0097 10.9447 34.4954C9.02506 33.9811 7.38785 32.7263 6.39227 31.0064ZM4.29707 13.6194C5.17156 12.0998 6.55279 10.9364 8.19885 10.3327C8.19885 10.4013 8.19491 10.5228 8.19491 10.6071V19.808C8.19351 20.0378 8.25334 20.2638 8.36823 20.4629C8.48312 20.6619 8.64893 20.8267 8.84863 20.9404L18.5723 26.5542L15.206 28.4979C15.1894 28.5089 15.1703 28.5155 15.1505 28.5173C15.1307 28.5191 15.1107 28.516 15.0924 28.5082L7.04046 23.8557C5.32135 22.8601 4.06716 21.2235 3.55289 19.3046C3.03862 17.3858 3.30624 15.3413 4.29707 13.6194ZM31.955 20.0556L22.2312 14.4411L25.5976 12.4981C25.6142 12.4872 25.6333 12.4805 25.6531 12.4787C25.6729 12.4769 25.6928 12.4801 25.7111 12.4879L33.7631 17.1364C34.9967 17.849 36.0017 18.8982 36.6606 20.1613C37.3194 21.4244 37.6047 22.849 37.4832 24.2684C37.3617 25.6878 36.8382 27.0432 35.9743 28.1759C35.1103 29.3086 33.9415 30.1717 32.6047 30.6641C32.6047 30.5947 32.6047 30.4733 32.6047 30.3889V21.188C32.6066 20.9586 32.5474 20.7328 32.4332 20.5338C32.319 20.3348 32.154 20.1698 31.955 20.0556ZM35.3055 15.0128C35.2464 14.9765 35.1431 14.9142 35.069 14.8717L27.1045 10.2712C26.906 10.1554 26.6803 10.0943 26.4504 10.0943C26.2206 10.0943 25.9948 10.1554 25.7963 10.2712L16.0726 15.8858V11.9982C16.0715 11.9783 16.0753 11.9585 16.0837 11.9405C16.0921 11.9225 16.1048 11.9068 16.1207 11.8949L24.1719 7.25025C25.4053 6.53903 26.8158 6.19376 28.2383 6.25482C29.6608 6.31589 31.0364 6.78077 32.2044 7.59508C33.3723 8.40939 34.2842 9.53945 34.8334 10.8531C35.3826 12.1667 35.5464 13.6095 35.3055 15.0128ZM14.2424 21.9419L10.8752 19.9981C10.8576 19.9893 10.8423 19.9763 10.8309 19.9602C10.8195 19.9441 10.8122 19.9254 10.8098 19.9058V10.6071C10.8107 9.18295 11.2173 7.78848 11.9819 6.58696C12.7466 5.38544 13.8377 4.42659 15.1275 3.82264C16.4173 3.21869 17.8524 2.99464 19.2649 3.1767C20.6775 3.35876 22.0089 3.93941 23.1034 4.85067C23.0427 4.88379 22.937 4.94215 22.8668 4.98473L14.9024 9.58517C14.7025 9.69878 14.5366 9.86356 14.4215 10.0626C14.3065 10.2616 14.2466 10.4877 14.2479 10.7175L14.2424 21.9419ZM16.071 17.9991L20.4018 15.4978L24.7325 17.9975V22.9985L20.4018 25.4983L16.071 22.9985V17.9991Z"
                                                                    fill="currentColor"></path>
                                                            </svg>
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="relative flex w-[calc(100%-50px)] flex-col gap-1 md:gap-3 lg:w-[calc(100%-115px)]">
                                                        <div class="flex flex-grow flex-col gap-3">
                                                            <!--  whitespace-pre-wrap -->
                                                            <div
                                                                class="min-h-[20px] flex flex-col items-start gap-4">

                                                                <div
                                                                    v-html="mdToHtml(conv.speeches[conv.idx], conv)"
                                                                    :class="{'result-streaming': conv.loading }"
                                                                    class="markdown prose-r width-full break-words dark:prose-invert light">
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                        <!--  举例  -->
                                        <div v-if="conversation.length ===0" @click="closeShowSlide"
                                             class="text-gray-700 width-full md:max-w-2xl lg:max-w-3xl md:h-full md:flex md:flex-col px-6 dark:text-gray-100 ">
                                            <div v-if="this.user_data.user_type === 'vip'">
                                                <h1 id="chatgpt" style="background-color: white"
                                                    class="text-4xl  text-center sm:mt-[20vh] ml-auto mr-auto mb-10 sm:mb-16 flex gap-2 items-center justify-center">
                                                    ChatGPT
                                                </h1>
                                            </div>
                                            <div v-else>
                                                <h1 id="chatgpt" style="background-color: white"
                                                    class="text-4xl  text-center sm:mt-[20vh] ml-auto mr-auto mb-10 sm:mb-16 flex gap-2 items-center justify-center">
                                                    ChatGPT<span id="plus">Plus</span>
                                                </h1>
                                            </div>

                                            <h2
                                                class="h-color m-bottom flex gap-3 items-center text-center m-auto text-lg font-normal md:flex-col items-center justify-center md:gap-2">
                                                <font-awesome-icon :icon="['fa', 'fa-blind']"
                                                                   style="width: 1.1rem;height: 1.1rem;color:#DA0719;"/>
                                                ChestNut
                                            </h2>
                                            <!--              ！！！！！！！！！！举例！！！！！！！！-->
                                            <div class="h-color md:flex items-start text-center gap-3.5 ">
                                                <div style="font-size: 0.9rem;"
                                                     class="flex flex-col  mb-8 md:mb-auto gap-3.5 flex-1">
                                                    <ul class="flex  flex-col gap-3.5 width-full sm:max-w-md m-auto">
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('世界十大不敢公开的灵异事件')"
                                                            class="cursor-pointer width-full h-but  bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-street-view']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            世界不敢公开的灵异事件
                                                            →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('巴西亚马逊外星人事件')"
                                                            class=" h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-street-view']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            巴西亚马逊外星人事件 →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('美国第五区事件')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-street-view']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            美国第五区事件
                                                            →
                                                        </button>
                                                    </ul>
                                                </div>
                                                <div style="font-size: 0.9rem;"
                                                     class="flex flex-col  mb-8 md:mb-auto gap-3.5 flex-1">
                                                    <ul class="flex flex-col gap-3.5 width-full sm:max-w-md m-auto">
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('特内里费空难')"
                                                            class=" h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-bicycle']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            特内里费空难 →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('世界十大奇案')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-bicycle']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            世界十大奇案 →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('营川坠龙事件')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-bicycle']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            营川坠龙事件
                                                            →
                                                        </button>
                                                    </ul>
                                                </div>
                                                <div style="font-size: 0.9rem;"
                                                     class="flex flex-col  m-left mb-8 md:mb-auto gap-3.5 flex-1">
                                                    <ul class="flex flex-col gap-3.5 width-full sm:max-w-md m-auto">
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('上海8·27UFO事件')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-trophy']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            上海8·27UFO事件 →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('914号航班失踪事件')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-trophy']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            914号航班失踪事件 →
                                                        </button>
                                                        <button
                                                            style="padding: 0.5rem;letter-spacing: 0.1rem;box-shadow: 1px 2px 4px rgb(2,2,2,0.3);"
                                                            @click="inputChat('英国航空9号班机事故')"
                                                            class="h-but cursor-pointer width-full bg-gray-20 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900">
                                                            <font-awesome-icon :icon="['fa', 'fa-trophy']"
                                                                               style="width: 0.8rem;height: 0.8rem;"/>
                                                            英国航空9号班机事故 →
                                                        </button>
                                                    </ul>
                                                </div>

                                            </div>
                                            <!--              ！！！！！！！！！！举例！！！！！！！！-->
                                        </div>
                                        <div style="" class="width-full h-32 md:h-48 flex-shrink-0"></div>
                                    </div>
                                    <transition name="el-fade-in-linear">
                                        <button v-show="isShowGotop" @click="handleScrolltop"
                                                class="cursor-pointer absolute right-6 bottom-[104px] md:bottom-[100px] z-10 rounded-full  text-gray-600   dark:text-gray-200">
                                            <font-awesome-icon :icon="['fa', 'fa-angle-double-up']" class="newchater4"/>
                                        </button>
                                    </transition>
                                    <transition name="el-fade-in-linear">
                                        <!-- 回到底部 -->
                                        <button v-show="isShowGoBottom" @click="handleScrollBottom"
                                                class="cursor-pointer absolute right-6 bottom-[124px] md:bottom-[120px] z-10 rounded-full   text-gray-600  dark:text-gray-200">
                                            <font-awesome-icon :icon="['fa', 'fa-angle-double-down']"
                                                               class="newchater4"/>
                                        </button>
                                    </transition>
                                </div>
                            </div>
                        </div>
                        <!--            输入框-->
                        <div
                            class="absolute bottom-0 left-0 width-full border-t md:border-t-0 dark:border-white/20 md:border-transparent md:dark:border-transparent md:bg-vert-light-gradient bg-white dark:bg-gray-800 md:!bg-transparent dark:md:bg-vert-dark-gradient"
                            style="border: none">
                            <form id="input"
                                  class=" mx-2 flex flex-row  gap-3 pt-2 last:mb-2 md:last:mb-6 lg:mx-auto lg:max-w-3xl lg:pt-6">
                                <div class="relative flex height-full flex-1 md:flex-col">
                                    <div class="flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center">
                                        <button v-if="!convLoading && conversation.length > 0"
                                                @click.stop.prevent="send(false)"
                                                id="chatRepeat"
                                                class="btn flex justify-center gap-2 btn-neutral border-0 md:border">
                                            <font-awesome-icon :icon="['fa', 'fa-spinner']"/>
                                            <p class="none" style="font-size: 0.8rem">reload</p>
                                        </button>
                                        <button v-if="convLoading" @click.stop.prevent="stopChat" id="stopChat"
                                                class="btn relative btn-neutral border-0 md:border">
                                            <div class="flex width-full items-center justify-center gap-2"
                                                 style="font-size: 0.8rem">
                                                <font-awesome-icon :icon="['fa', 'fa-refresh']"/>
                                                stop
                                            </div>
                                        </button>
                                    </div>
                                    <div
                                        class="flex flex-col width-full py-2 flex-grow md:py-3 md:pl-4 relative border border-black/10 dark:border-gray-900/50 dark:text-white dark:bg-gray-700 rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)] dark:shadow-[0_0_15px_rgba(0,0,0,0.10)]"
                                        >
                    <textarea id="textare" v-model="chatMsg" ref="inputChat" placeholder="请输入内容，进行对话"
                              @keydown="judgeInput" tabindex="0"
                              data-id="root"
                              style="max-height: 200px; height: 24px; overflow-y: hidden;" rows="1"
                              class="m-0 width-full text1 resize-none border-0 bg-transparent p-0 pl-2 pr-7 focus:ring-0 focus-visible:ring-0 md:pl-0"></textarea>
                                        <button id="btn-send" @click.stop.prevent="send" :disabled="convLoading"
                                                class="absolute p-1 rounded-md bottom-1.5 right-1 md:bottom-2.5 md:right-2">
                                            <div v-if="convLoading" class="text-2xl" style="line-height: 1.3rem;">
                                                <span class="load_dot1">·</span><span class="load_dot2">·</span><span
                                                class="load_dot3">·</span>
                                            </div>
                                            <font-awesome-icon :icon="['fa', 'paper-plane']"/>
                                        </button>
                                    </div>
                                </div>
                            </form>
                            <div
                                class="px-3 pt-2  text-center text-xs text-black/50 dark:text-white/50 md:px-4 md:pt-3 md:pb-6">
                                Copyright &copy; TwinParticle-MegaCosmo 2023
                            </div>
                        </div>
                    </main>
                </div>
                <!--        菜单导航栏-->
                <div class="dark hidden bg-gray-900 md:fixed md:inset-y-0 md:flex md:w-[260px] md:flex-col"
                     style="border-radius: 0px 10px 10px 0px">
                    <div class="daohangmark">
                        <div ref="menu"
                             class="scrollbar-trigger flex height-full width-full flex-1 items-start border-white/20 ">
                            <nav ref="navEle" class="flex height-full flex-1 flex-col space-y-1 p-2 grey_xxx">
                                <a @click.stop="newChat"
                                   class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm mb-2 flex-shrink-0 border border-white/20">
                                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                                         stroke-linecap="round"
                                         stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                         xmlns="http://www.w3.org/2000/svg">
                                        <line x1="12" y1="5" x2="12" y2="19"></line>
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                    </svg>
                                    点击对话（New）
                                </a>
                                <!-- 对话列表 -->
                                <!--  对话存储              -->
                                <div class="save-chat border-white/20" style="padding-bottom: 5px;">
                                    <div class="save-chat-1 text-gray-100 text-sm">
                                        <template v-for="(conversation, cidx) in conversations">
                                            <!--                      编辑对话存储-->
                                            <div v-if="conversation.editable"
                                                 class="m-focus flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer hover:pr-14 break-all pr-14 bg-gray-800 hover:bg-gray-800">
                                                <svg stroke="currentColor" fill="none" stroke-width="2"
                                                     viewBox="0 0 24 24"
                                                     stroke-linecap="round"
                                                     stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                        d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z">
                                                    </path>
                                                </svg>
                                                <input id="titleInput" v-model="convTitletmp"
                                                       @blur="titleInputBlur(cidx, conversation)"
                                                       type="text"
                                                       class="text-sm border-none bg-transparent p-0 m-0 width-full mr-0"
                                                       autofocus="true">
                                                <div class="absolute flex right-1 z-10 text-gray-300 visible">
                                                    <button @click="changeConvTitle(cidx, conversation)"
                                                            class="p-1 hover:text-white">
                                                        <font-awesome-icon :icon="['fa', 'fa-check']"/>
                                                    </button>
                                                    <button @click="cancelChangeConvTitle(cidx, conversation)"
                                                            class="p-1 hover:text-white">
                                                        <font-awesome-icon :icon="['fa', 'fa-remove']"/>
                                                    </button>
                                                </div>
                                            </div>
                                            <!--                      编辑对话删除-->
                                            <a v-else-if="conversation.delete" @blur="cancelDelConv(cidx, conversation)"
                                               class="m-focus flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all pr-14 bg-gray-800 hover:bg-gray-800 group">
                                                <font-awesome-icon :icon="['fa', 'fa-trash']"/>
                                                <div
                                                    class="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative">
                                                    删除
                                                    "{{ conversation.title }}"?
                                                    <div
                                                        class="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l from-gray-800"></div>
                                                </div>
                                                <div class="absolute flex right-1 z-10 text-gray-300 visible">
                                                    <button @click="delConv(cidx,conversation)"
                                                            class="p-1 hover:text-white">
                                                        <font-awesome-icon :icon="['fa', 'fa-check']"/>
                                                    </button>
                                                    <button @click="cancelDelConv(cidx, conversation)"
                                                            class="p-1 hover:text-white">
                                                        <font-awesome-icon :icon="['fa', 'fa-remove']"/>
                                                    </button>
                                                </div>
                                            </a>
                                            <!--                      选择对话框-->
                                            <a v-else @click.stop.prevent="selectConversation(conversation, true, true)"
                                               :class="{ 'bg-gray-800 hover:bg-gray-800 pr-14': conversation.selected, 'hover:bg-[#2A2B32] hover:pr-4': !conversation.selected }"
                                               class="flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all group">
                                                <svg stroke="currentColor" fill="none" stroke-width="2"
                                                     viewBox="0 0 24 24"
                                                     stroke-linecap="round"
                                                     stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                        d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z">
                                                    </path>
                                                </svg>
                                                <div @click="history_func"
                                                     class="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative">
                                                    {{ conversation.title }}
                                                    <div
                                                        :class="{ 'from-gray-800': conversation.selected, 'from-gray-900 group-hover:from-[#2A2B32]': !conversation.selected }"
                                                        class="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l">
                                                    </div>
                                                </div>
                                                <div v-show="conversation.selected"
                                                     class="absolute flex right-1 z-10 text-gray-300 visible">
                                                    <button @click="conversation.delete = true"
                                                            class="p-1 hover:text-white">
                                                        <font-awesome-icon :icon="['fa', 'fa-trash']"/>
                                                    </button>
                                                </div>
                                            </a>
                                        </template>
                                    </div>

                                </div>
                                <!--   清除对话             -->
                                <a v-if="conversations.length > 0" @click.stop.prevent="clearConversations"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                                         stroke-linecap="round"
                                         stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                         xmlns="http://www.w3.org/2000/svg">
                                        <polyline points="3 6 5 6 21 6"></polyline>
                                        <path
                                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                                        </path>
                                        <line x1="10" y1="11" x2="10" y2="17"></line>
                                        <line x1="14" y1="11" x2="14" y2="17"></line>
                                    </svg>
                                    清空对话（Clean Up）
                                </a>
                                <!--  夜间模式切换              -->
                                <a v-if="theme === 'light'" @click="changeTheme('dark')"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                                         stroke-linecap="round"
                                         stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                         xmlns="http://www.w3.org/2000/svg">
                                        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                                    </svg>
                                    深色模式（Trun Off）
                                </a>
                                <a v-if="theme === 'dark'" @click="changeTheme('light')"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                                         stroke-linecap="round"
                                         stroke-linejoin="round" class="newchater" height="1em" width="1em"
                                         xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="12" cy="12" r="5"></circle>
                                        <line x1="12" y1="1" x2="12" y2="3"></line>
                                        <line x1="12" y1="21" x2="12" y2="23"></line>
                                        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                                        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                                        <line x1="1" y1="12" x2="3" y2="12"></line>
                                        <line x1="21" y1="12" x2="23" y2="12"></line>
                                        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                                        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                                    </svg>
                                    浅色模式（Turn On）
                                </a>
                                <a @click="chooseone" id="payfor"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <font-awesome-icon :icon="['fa', 'fa-ship']"/>
                                    订阅会员（Upgrade）
                                </a>

                                <a @click="feedback" id="feedback1"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <font-awesome-icon :icon="['fa', 'fa-train']"/>
                                    反馈（Feedback）
                                </a>
                                <center>
                                    <div id="choose" class="close">
                                        <div id="model-content-choose">
                                            <div class="button-normal button-subscirbe">
                                                <span class="subscribe-title">教育优惠</span>
                                                <span class="original-price">原价：<span
                                                    style="text-decoration: line-through; color: darkred; font-weight: bold">¥ 68.00</span></span>
                                                <div class="price-month">
                                                    <h1 class="current-price">¥ 35.00</h1>
                                                    <label class="per-month"> /月</label>
                                                </div>
                                                <button v-if="!this.user_data.is_edu" type="button"
                                                        class="button-all-sm" id="edu-check"
                                                        @click="upgrade('教育优惠', '35.00')">立即认证
                                                </button>
                                                <button v-else type="button" class="button-all-sm" id="edu-check"
                                                        @click="upgrade('教育优惠', '35.00')">立即订阅
                                                </button>
                                                <ul class="subscribe-info-list">
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        学生教师认证后可享受
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        GPT-3 Turbo引擎
                                                    </li>
                                                    <!--                                                    <li class="subscribe-info-item">-->
                                                    <!--                                                        <svg stroke="currentColor" fill="none" stroke-width="2"-->
                                                    <!--                                                             viewBox="0 0 24 24"-->
                                                    <!--                                                             stroke-linecap="round" stroke-linejoin="round"-->
                                                    <!--                                                             class="subscribe-item-icon"-->
                                                    <!--                                                             height="1em" width="1em"-->
                                                    <!--                                                             xmlns="http://www.w3.org/2000/svg">-->
                                                    <!--                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>-->
                                                    <!--                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>-->
                                                    <!--                                                        </svg>-->
                                                    <!--                                                        更快响应时间-->
                                                    <!--                                                    </li>-->

                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        无限制连续对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        WeChat公众号直接对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-erro-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <line x1="18" y1="6" x2="6" y2="18"></line>
                                                            <line x1="6" y1="6" x2="18" y2="18"></line>
                                                        </svg>
                                                        GPT4引擎
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-erro-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <line x1="18" y1="6" x2="6" y2="18"></line>
                                                            <line x1="6" y1="6" x2="18" y2="18"></line>
                                                        </svg>
                                                        AI创意绘画
                                                    </li>
                                                </ul>
                                            </div>
                                            <div class="button-normal button-subscirbe">
                                                <span class="subscribe-title">标准会员</span>
                                                <span class="original-price">原价：<span
                                                    style="text-decoration: line-through; color: darkred; font-weight: bold">¥ 108.88</span></span>
                                                <div class="price-month">
                                                    <!--                                                    <div class="text-container">-->
                                                    <h1 class="current-price">¥</h1>
                                                    <h1 class="current-price"
                                                        style="text-decoration: line-through;color: darkred">68.00</h1>
                                                    <h1 class="current-price">35.00</h1>
                                                    <label class="per-month"> /月</label>
                                                    <!--                                                    </div>-->
                                                </div>
                                                <button type="button" class="button-all-sm" id="normal"
                                                        @click="upgrade('标准会员', '35.00')">
                                                    🔥限时优惠
                                                </button>
                                                <ul class="subscribe-info-list">
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        GPT-3 Turbo引擎
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        更快响应时间
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        无限制连续对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        WeChat公众号直接对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-erro-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <line x1="18" y1="6" x2="6" y2="18"></line>
                                                            <line x1="6" y1="6" x2="18" y2="18"></line>
                                                        </svg>
                                                        GPT4引擎
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-erro-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <line x1="18" y1="6" x2="6" y2="18"></line>
                                                            <line x1="6" y1="6" x2="18" y2="18"></line>
                                                        </svg>
                                                        AI创意绘画
                                                    </li>
                                                </ul>
                                            </div>
                                            <div class="button-normal button-subscirbe">
                                                <span class="subscribe-title">专业会员</span>
                                                <span class="original-price">原价：<span
                                                    style="text-decoration: line-through; color: darkred; font-weight: bold">¥ 208.88</span></span>
                                                <!--                                                <h1 class="current-price">¥ 168.00</h1>-->
                                                <div class="price-month">
                                                    <h1 class="current-price">¥ 168.00</h1>
                                                    <label class="per-month"> /月</label>
                                                </div>
                                                <button type="button" class="button-all-sm" id="super"
                                                        @click="upgrade('专业会员', '168.00')">
                                                    立即尊享
                                                </button>
                                                <ul class="subscribe-info-list">
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        GPT-3 Turbo引擎
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        更快响应时间
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        无限制连续对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        WeChat公众号直接对话
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        GPT4专业引擎
                                                    </li>
                                                    <li class="subscribe-info-item">
                                                        <svg stroke="currentColor" fill="none" stroke-width="2"
                                                             viewBox="0 0 24 24"
                                                             stroke-linecap="round" stroke-linejoin="round"
                                                             class="subscribe-item-icon"
                                                             height="1em" width="1em"
                                                             xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                                                        </svg>
                                                        AI创意绘画 5张/月
                                                    </li>
                                                </ul>
                                            </div>
                                            <!--                     教育认证-->
                                            <!--                    <a id="wefive-a" @click="checkemial" onmouseover="this.style.textDecoration='none'"-->
                                            <!--                       onmouseout="this.style.textDecoration='underline'">您可以点击链接进行教育认证!</a>-->
                                        </div>
                                    </div>
                                </center>
                                <!--支付界面               -->
                                <div id="casher" class="model1">
                                    <div class="model1-content">
                                        <div class="reselect-plan-btn-container">
                                            <div class="casher-top">
                                                <div @click="reChooseOne();" class="reselect-plan-btn" type="button">&lt
                                                    当前方案：{{ this.upgrade_scheme_describe }}
                                                </div>
                                                <!--                                                <span class="close-casher-X" @click="closeEduEmail">X</span>-->

                                            </div>
                                        </div>
                                        <!--                      <span class="casher-info">当前方案: <span class="current-scheme">教育优惠</span></span>-->
                                        <span class="current-scheme">¥ {{ this.upgrade_scheme_amount }}</span>
                                        <div class="pay-info">———— 支付方式 ————</div>
                                        <div class="payment-box">
                                            <button @click="choseAliPay" class="payment alipay "
                                                    :class="{active: alipay_is_active, 'alipay-hover': !alipay_is_active}">
                                                <i class="fa-brands fa-alipay"
                                                   style="font-size: 1.3rem;vertical-align: -1px;margin-right: 2px;"></i>&nbsp;&nbsp;支付宝&nbsp;&nbsp;
                                            </button>
                                            <div @click="choseWechatPay" class="payment wechat-pay"
                                                 :class="{active: wechat_is_active, 'wechat-pay-hover': !wechat_is_active}">
                                                <i class="fa-brands fa-weixin" style="font-size: 1.3rem"></i>&nbsp;微信支付
                                            </div>
                                        </div>
                                        <p v-if="alipay_is_active" style="color:black;">
                                            点击「立即支付」后请在新页面进行操作...</p>
                                        <p v-if="pay_erro" style="color: darkred">请先选择支付方式 !</p>
                                        <button @click="payForIt" class="pay-now">立即支付</button>
                                    </div>
                                    <div class="model2-content">
                                        <span class="pay-tip" v-if="isWeChatBrowser">正在处理...</span>
                                        <span class="pay-tip" v-else-if="wechat_is_active">请打开 「微信」 扫码支付</span>
                                        <span class="pay-tip" v-else>请在新页面完成操作,正在等待支付完成</span>

                                        <div :class="{'pay-card': wechat_is_active}">
                                            <div v-if="wechat_is_active&&!isWeChatBrowser" class="pay-amount">
                                                {{ this.upgrade_scheme_amount }} CNY
                                            </div>
                                            <div class="qr-img-container">
                                                <img class="qr-img" :class="{'loading-spinner': !is_loading_qr_img}"
                                                     src="./assets/imgs/loading.svg">
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <!--                                        教育认证-->
                                <div id="wefive-a-check" class="model2">
                                    <div v-if="request_is_loading" id="wefive-a-check-content">
                                        <img id="request-loading" class="loading-spinner  "
                                             src="./assets/imgs/loading.svg">
                                        <span style="color:#000; margin: 3rem">正在处理,请稍等...</span>
                                    </div>

                                    <div v-else id="wefive-a-check-content">
                                        <span class="closeEduX" @click="closeEduEmail">X</span>
                                        <span class="edu-tip">请先完成教育认证</span>
                                        <form id="formcheck">
                                            <div class="input-tips">
                                                <label class="tip-info">Email</label>
                                                <input
                                                    id="input-email"
                                                    placeholder="请输入教育邮箱">
                                            </div>
                                            <div class="input-tips">
                                                <label class="tip-info">验证码</label>
                                                <div class="input-code-box">
                                                    <input id="input-test" class="input-code"
                                                           placeholder="请先获取验证码">
                                                    <button id="btn-test" type="button" @click="sendCode"
                                                            class="get-code-btn">获取验证码
                                                    </button>
                                                </div>
                                            </div>
                                            <span v-if="is_erro_msg"
                                                  style="color: darkred; margin-top: 1rem">{{ erro_msg }}</span>
                                            <span v-if="is_msg" style="color: darkgreen; margin-top: 1rem">{{
                                                    msg
                                                }}</span>

                                            <button id="btn-check" type="button" class="check-btn"
                                                    @click="checksub">立即认证
                                            </button>
                                        </form>
                                    </div>

                                </div>

                                <div id="wxin">
                                    <div id="weixin-pay" class="zhifubao-pay">
                                        <img id="we-wechat" class="we-pic"/>
                                        <div id="mone-wechat" class="mone">价格:<span id="money-wechat"></span>元</div>
                                        <h5 id="wefive-wechat" class="wefive">使用手机微信扫描二维码安全支付</h5>
                                    </div>
                                </div>
                                <div id="fed">
                                    <div id="fed-content">
                                        <h3 id="h1-fed" style="text-align: center;color: #0C001C">反馈（Feedback）</h3>
                                        <form id="fedform">
                                            <textarea id="fed-text"
                                                      placeholder="请输入反馈内容，我们珍视每一条反馈意见~"></textarea>
                                        </form>
                                        <button @click="subfedback" type="button" class="items-center" id="sub-fed">
                                            提交
                                        </button>
                                    </div>
                                </div>
                                <!--                手动登录-->
                                <!--                <a @click="showLoginModal1" id="login"-->
                                <!--                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">-->
                                <!--                  <font-awesome-icon :icon="['fa', 'fa-rocket']"/>-->
                                <!--                  Login-->
                                <!--                </a>-->
                                <a @click="logout" id="logout"
                                   class="flex py-33 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm1">
                                    <font-awesome-icon :icon="['fa', 'fa-hourglass-half']"/>
                                    登出（Exit）
                                </a>

                            </nav>
                        </div>
                    </div>
                </div>
                <!--间隔线-->
            </div>
            <div id="sec" class="app-sec"></div>
        </div>
        <!--    关闭菜单栏-->
        <div v-show="showSlide" class="semi-portal" style="z-index: 600;">
            <div class="">
                <div class="semi-modal-mask"></div>
                <div role="none" class="semi-modal-wrap">
                    <div class="semi-modal semi-modal-small" id="dialog-3" style="width: 0px;">
                        <div role="dialog" aria-modal="true" aria-labelledby="semi-modal-title"
                             aria-describedby="semi-modal-body"
                             class="semi-modal-content">
                            <div class="semi-modal-body-wrapper">

                                <div class="semi-modal-body" x-semi-prop="children">

                                    <div class="fixed inset-0 z-40 flex">

                                        <div
                                            class="relative flex width-full max-w-xs flex-1 flex-col bg-gray-900  translate-x-0"
                                            id="headlessui-dialog-panel-:r1:" data-headlessui-state="open">
                                            <!--                      <div class="absolute top-0 right-0 -mr-12 pt-2 opacity-100">-->
                                            <!--                        <button @click="closeShowSlide" type="button"-->
                                            <!--                                class="ml-1 flex h-10 w-10 items-center justify-center"><span-->
                                            <!--                            class="sr-only">Close sidebar</span>-->
                                            <!--                          <svg stroke="currentColor" fill="none" stroke-width="1.5" viewBox="0 0 32 32"-->
                                            <!--                               stroke-linecap="round" stroke-linejoin="round" class="newchater-2 text-white"-->
                                            <!--                               height="1em"-->
                                            <!--                               width="1em" xmlns="http://www.w3.org/2000/svg">-->
                                            <!--                            <line x1="18" y1="6" x2="6" y2="18"></line>-->
                                            <!--                            <line x1="6" y1="6" x2="18" y2="18"></line>-->
                                            <!--                          </svg>-->
                                            <!--                        </button>-->
                                            <!--                      </div>-->
                                            <div ref="slideNavContainer" style="width:280px"
                                                 class="flex height-full flex-1 items-start border-white/20 grey_xxx"
                                                 id="slider">
                                            </div>
                                        </div>
                                        <div @click="closeShowSlide" style="width:calc(100% - 320px)"
                                             class="flex-shrink-0"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div portal-container="">
      <span
          class="pointer-events-none fixed inset-0 z-[60] mx-auto my-2 flex max-w-[560px] flex-col items-stretch justify-start md:pb-5">
      </span>
        </div>
    </div>
    <div id="tanchuang" v-bind="jugelogin">
        <div id="show-login">
            <div id="show-login-content">
                <img id="load-login" class="loading-spinner login-loading " src="./assets/imgs/loading.svg">
                <img id="we1"/>
                <h5 id="wefive2">使用手机微信扫码安全登录</h5>
            </div>
        </div>
    </div>
</template>
<script>
import './assets/index.css'
import 'highlight.js/styles/github-dark.css';
import hljs from "highlight.js";
import {marked} from "marked";
import 'github-markdown-css';
import 'whatwg-fetch';
import {testWebpack5} from "vue-loader/dist/util";


hljs.initHighlightingOnLoad();

const renderer = {
    code(code, infostring) {
        var codeHtml = code;
        if (infostring) {
            codeHtml = hljs.highlightAuto(code).value;
        }

        return `<div class="bg-black mb-4 rounded-md" >
      <div class="code_header flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans">
        <span>${infostring || ""}</span>
        <button onclick="copy(this)" class="flex ml-auto gap-2">
          <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
          </svg>
          <span>Copy code</span>
          <code style="display:none">${code}</code>
        </button>
      </div>
      <div class="p-4 overflow-y-auto">
        <code class="!whitespace-pre hljs ${infostring}">${codeHtml}</code>
      </div>
    </div>`;
    },
    paragraph(text) {
        return `<p>${text}</p>`;
    }
};

marked.use({renderer});


marked.setOptions({
    highlight: function (code, lang) {
        //此处的highlight.js不需要额外引入,marked自带highlight.js
        // const hljs = require("highlight.js");
        // // // console.log("code=", code, "lang=", lang,'hljs.highlight',hljs.highlight);
        const result = lang&&highlightSupportLang.includes(lang)?hljs.highlight(code,{language:lang}).value:hljs.highlightAuto(code).value;
        return result;
    },
    langPrefix: "hljs language-",
    // highlight.js css expects a top-level 'hljs' class.
});


export default {
    data() {
        return {
            theme: "light",
            popupShow: true,
            avatarIdx: 1,
            conversations: [],
            current_chat_id: null,
            conversation: [],
            chatMsg: "",
            chatTitle: "New chat",
            convLoading: false,
            showSlide: false,
            isShowGoBottom: false,
            oldConv: undefined,
            convTitletmp: "",
            source: undefined,
            rsource: undefined,
            tsource: undefined,
            chat_id: "",
            imgs: [
                "./src/assets/imgs/user1.png",
                "./src/assets/imgs/user3.png",
                "./src/assets/imgs/user6.png",
                "./src/assets/imgs/user2.png",
                "./src/assets/imgs/user5.png",
                "./src/assets/imgs/user7.png",
                "./src/assets/imgs/user8.png",
            ],
            isShowGotop: false,
            nums: 10,
            clock: "",
            btn: "",
            code_login: "",
            login_id: "",
            token_id: "",
            token_msg: "",
            code: "",
            pay_id: "",
            old_chat: "",
            stop_single: false,
            alipay_is_active: false,
            wechat_is_active: false,
            is_new_chat: true,
            is_load_to_login: true,
            request_is_loading: false,
            pay_erro: false,
            is_erro_msg: false,
            erro_msg: '',
            is_msg: false,
            msg: '',
            user_data: {},
            upgrade_scheme_describe: "",
            upgrade_scheme_amount: "0.00",
            is_loading_qr_img: false,
            isWeChatBrowser: false,
        };

    },
    methods: {
        testWebpack5,
        handleScrolltop() {
            this.$nextTick(() => {
                let scrollElem = this.$refs.chatContainer;
                scrollElem.scrollTo({top: 0, behavior: 'smooth'});
            });
        },
        JudgeWechatBrowser() {
            var userAgent = navigator.userAgent.toLowerCase();
            // // // console.log(userAgent);
            if (userAgent.indexOf("micromessenger") !== -1) {
                this.isWeChatBrowser = true;
                // alert("在微信内置浏览器中");
            } else {
                this.isWeChatBrowser = false;
                // alert("在非微信内置浏览器中");
            }
        },
        isScrollAndNottop() {
            let chatDivEle = this.$refs.chatContainer;
            if (!chatDivEle) {
                return;
            }
            if (chatDivEle.scrollHeight <= chatDivEle.clientHeight) {
                this.isShowGotop = true;
                return;
            }
            const scrollTop = chatDivEle.scrollTop;
            const windowHeight = chatDivEle.clientHeight;
            const scrollHeight = chatDivEle.scrollHeight;
            if (scrollTop + windowHeight >= scrollHeight - 50) {
                this.isShowGotop = true;
                return;
            }
            this.isShowGotop = false;
        },
        stopChat() {
            this.stop_single = true;
            var that = this;
            var controller = new AbortController();
            var rconv = this.conversation[this.conversation.length - 1];
            rconv["loading"] = false;
            this.convLoading = false;
            if (that.conversation.length === 2 && rconv["speeches"].length === 1) {
                var newConv = {
                    "id": that.cid,
                    "title": "New chat"
                }
                that.generateConvTitle(newConv);
                that.conversations.unshift(newConv);
                that.selectConversation(newConv, false);
                that.saveConversations();
            }
            that.refrechConversation();
            controller.abort()
        },
        closeShowSlide() {
            this.showSlide = false;
            this.$refs.menu.appendChild(this.$refs.navEle);
        },
        showSlideMethod() {
            var that = this;
            this.showSlide = true;
            this.$refs.slideNavContainer.appendChild(this.$refs.navEle);

            // 添加全屏元素
            // document.
            // 绑定事件监听

            // const el = document.getElementsByClassName("close");
            // el.style.display = "block";
            //   点击其他领域(即弹窗背景)
            // document.addEventListener('click', function (event) {
            //   // // // console.log('click...', event.target, el);
            //   // // // console.log(event.target.classes);
            //
            //   if (event.target.className.indexOf("close")) {
            //     that.closeShowSlide();
            //     // 获取所有click事件监听器
            //     document
            //         .querySelectorAll("*")
            //         .forEach(node =>
            //             node.addEventListener(
            //                 "click",
            //                 event => event.stopImmediatePropagation(),
            //                 true
            //             )
            //         );
            //   }
            // });

        },
        changeHeight() {
            var elem = this.$refs.inputChat;
            elem.style.height = '24px';
            var scrollHeight = elem.scrollHeight;
            if (24 >= scrollHeight || this.chatMsg.length === 0) {
                this.resetHeight();
                return;
            }

            elem.style.removeProperty("overflow-y")
            elem.style.height = scrollHeight + 'px';
        },
        resetHeight() {
            var elem = this.$refs.inputChat;
            elem.style.height = '24px';
            elem.style["overflow-y"] = 'hidden';
        },
        vueCopy(node) {
            var code = node.getElementsByTagName("code")[0].innerHTML
            var text = decodeURIComponent(code);
            this.$copyText(text).then(
                res => {
                    var svg = `<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span>Copied!</span>`
                    const nodeInnerHtml = node.innerHTML
                    node.innerHTML = svg;
                    setTimeout(() => {
                        node.innerHTML = nodeInnerHtml
                    }, 1000);
                },
                err => {
                    // // // console.log('复制失败');
                }
            );
        },
        changeTheme(theme) {
            this.theme = theme;
            var html = document.getElementsByTagName("html")[0]
            html.classList.remove("light", "dark");
            html.classList.add(theme);
            html.style["color-scheme"] = theme;
            localStorage.setItem("theme", theme)
        },
        // 有角色区分
        initConvs(convs) {
            var that = this
            var con = []
            for (let i = 0; i < convs.length; i++) {
                var conv = convs[i];
                if (conv.user) {
                    con.push({
                        "speaker": "user",
                        "speech": conv.user
                    })
                    if (conv.assitant) {
                        con.push({
                            "idx": 0,
                            "loading": false,
                            "speaker": "assitant",
                            "suitable": [0],
                            "speeches": [conv.assitant]
                        })
                    }
                }
            }
            return con
        },
        last(conv) {
            if (conv.idx === 0) {
                return;
            }
            conv.idx--;
            this.refrechConversation();
        },
        next(conv) {
            if (conv.idx === conv["speeches"].length - 1) {
                return;
            }
            conv.idx++;
            this.refrechConversation();
        },
        inputChat(msg) {
            // // // console.log(msg);
            this.chatMsg = msg;
        },
        countAndConcat(str, substr) {
            // 使用正则表达式的全局匹配来查找子字符串
            const matches = str.match(new RegExp(substr, 'g'));

            // 判断子字符串的个数是奇数还是偶数
            const count = matches ? matches.length : 0;
            const isOdd = count % 2 === 1;

            // 根据判断结果返回相应的字符串
            return isOdd ? str + "\n" + substr : str;
        },
        mdToHtml(md, conv) {
            // md = md.replace(/'/g, '&#39;'); // 替换单引号
            // md = md.replace(/"/g, '&#34;'); // 替换双引号
            if (md === "") {
                return "<p></p>"
            }
            md = this.countAndConcat(md, "```")
            var htmlMD = marked.parse(md);
            htmlMD = htmlMD.trim();
            return htmlMD;
        },
        markdown(raw_text) {
            var marked_html = sconverter.makeHtml(text);
        },

        refrechConversation() {
            this.conversation = JSON.parse(JSON.stringify(this.conversation));
        },
        judgeInput(e) {
            if (!e.shiftKey && e.keyCode === 13) {
                e.cancelBubble = true;  //ie阻止冒泡行为
                e.stopPropagation(); //Firefox阻止冒泡行为
                e.preventDefault(); //取消事件的默认动作*换行
                this.send(true);
            }
        },
        // 发送消息
        async send(is_send) {
            // console.log('this.is_new_chat:', this.is_new_chat)
            // 滚动到最下面
            this.handleScrollBottom();
            var that = this
            this.convLoading = true;
            if (is_send) {
                localStorage.setItem('chatmsg', this.chatMsg);
            }
            this.chatMsg = ""
            this.conversation.push({
                "speaker": "user",
                "speech": localStorage.getItem('chatmsg')
            })
            var conv = {
                "idx": 0,
                "loading": true,
                "speaker": "assitant",
                "suitable": [0],
                "speeches": [""]
            }
            this.conversation.push(conv);

            var controller = new AbortController();

            if (this.is_new_chat) {
                this.current_chat_id = null;
            }

            var token = localStorage.getItem('token');

            const response = await fetch('https://api.tpcosmo.com/chat_stream', {
                method: "POST",
                body: JSON.stringify({
                    "content": localStorage.getItem('chatmsg'),
                    "chat_id": this.current_chat_id
                }),
                headers: {
                    'token': token,
                    "Content-Type": "application/json"
                },
            });

            //获取UTF8的解码
            const encode = new TextDecoder("utf-8");
            //获取body的reader
            const reader = response.body.getReader();


            // 循环读取reponse中的内容
            while (true) {
                // 刷新new id

                // this.is_new_chat = false;
                const {done, value} = await reader.read();
                if (done) {
                    // 滚动到最下面
                    this.handleScrollBottom();
                    that.stop_single = false;
                    // return;
                    break;
                }
                // 解码内容
                const text = encode.decode(value);
                // // // console.log("接受消息： ", text);

                var conv = that.conversation[that.conversation.length - 1];
                // that.handleScrollBottom();

                if (that.stop_single) {
                    that.stop_single = false;
                    break;
                }

                conv["speeches"][0] += text;
                controller.abort();
                conv["loading"] = false;
                that.convLoading = false;

                that.refrechConversation();

            }
            if (this.is_new_chat) {
                // // // console.log('准备刷新侧边栏...')
                this.getSidebarTitles();
                this.is_new_chat = false;
            }
        },
        generateConvTitle(conv) {
            conv.title = ""
            var chat1 = localStorage.getItem('chatmsg')
            conv.title = chat1.slice(0, 10)
            this.selectConversation(conv, false);
            this.saveConversations()
        },
        // 666666666666666666666

        selectConversation(conv, loadConv, modify) {
            modify = modify || false;

            var that = this;
            this.is_new_chat = false;
            // 如果已经有旧的对话，将其选中状态设为false
            if (this.oldConv) {
                this.oldConv.selected = false;
            }
            // 将当前对话设为选中状态
            conv.selected = true
            // 将当前对话设为旧的对话
            this.oldConv = conv;
            // 设置页面标题和聊天标题
            // document.title = conv.title || "New Chat";
            if (modify) {
                this.chatTitle = conv.title || "New CHat";
            }
            // 如果不需要加载对话，直接返回
            if (!loadConv) {
                return;
            }
            var token = localStorage.getItem('token');
            var convId = conv.chat_id;
            this.current_chat_id = convId;
            // localStorage.setItem('chatid', convId)

            this.axios.post("https://api.tpcosmo.com/chat_content",
                {
                    "chat_id": convId, // 对话ID
                    "page_size": 10, // 对话数量，最大为5
                    "page": 1 // 页数

                }, {
                    headers: {
                        "token": token,
                        'Content-Type': 'application/json'
                    }
                }).then((result) => {
                var resu = result.data
                if (resu.code === 200) {
                    var resuu = resu.data
                    // 显示历史对话记录
                    that.cid = conv.chat_id
                    that.conversation = that.initConvs(resuu);
                    that.convLoading = false;

                    setTimeout(() => {
                        that.isScrollAndNotBottom();
                    }, 300)
                }
            })
            // 加载历史对话记录
        },
        getSidebarTitles() {
            var that = this;
            var token = localStorage.getItem('token')
            this.axios.post("https://api.tpcosmo.com/chat_list", {"page": 1, "page_size": 10}, {
                headers: {
                    "token": token
                }
            }).then((result) => {
                var resu = result.data
                if (resu.code === 200) {
                    var r = resu.data
                    // that.conversations = r;
                    that.saveConversations()
                    var oldid = [];
                    that.conversations = [];
                    for (var i = 0; i < r.length; i++) {
                        // this.saveConversations()
                        that.addSidebarTitle(r[i].chat_id, r[i].title);
                        oldid.push(r[i].chat_id);
                        that.conversations.unshift(r[i])
                    }
                    localStorage.setItem('oldid', JSON.stringify(oldid));
                    this.current_chat_id = this.conversations[0].chat_id

                    // if (this.is_new_chat) {
                    //     this.current_chat_id = this.conversations[0].chat_id
                    // }
                }
            })
        },
        // 6666666666获取新的会话id
        addSidebarTitle(id, title) {
            var newConv = {
                "chat_id": id,
                "title": title
            }
            this.selectConversation(newConv, false, false);
        },
        saveConversations() {
            var that = this
            var conversations = JSON.parse(JSON.stringify(that.conversations));
            for (let idx in conversations) {
                var conv = conversations[idx];
                delete conv.editable;
                delete conv.selected;
                delete conv.delete;
            }
            let convs = JSON.stringify(conversations);
            // localStorage.setItem("conversations", convs);
        },
        // 6666666666666666666conv6
        clearConversations() {
            this.newChat();
            this.conversations = [];
            this.saveConversations();
            var that = this;
            var token = localStorage.getItem('token')
            var chat_id = eval(localStorage.getItem('oldid'))
            // // // console.log(chat_id)
            this.axios.post("https://api.tpcosmo.com/clean", {"data": null}, {
                headers: {
                    "token": token,
                }
            }).then(function (response) {
                var respon = response.data
                if (respon.code === 200) {
                }
            })
        },
        titleInputBlur(idx, conv) {
            setTimeout(() => {
                this.cancelChangeConvTitle(idx, conv);
            }, 100);
        },
        changeConvTitle(idx, conv) {
            conv.title = this.convTitletmp;
            this.saveConversations();
            this.cancelChangeConvTitle(idx, conv);
        },
        cancelChangeConvTitle(idx, conv) {
            conv.editable = false;
            var that = this
            that.$set(that.conversations, idx, conv);
        },
        delConv(cidx, conv) {
            this.conversations.splice(cidx, 1);
            this.saveConversations();
            var token = localStorage.getItem('token')
            var chat_id = []
            chat_id.push(conv.chat_id)
            // // // console.log(chat_id)
            this.axios.post("https://api.tpcosmo.com/clean", {"data": chat_id}, {
                headers: {
                    "token": token,
                }
            }).then(function (response) {
                var respon = response.data
                if (respon.code === 200) {
                }
            })
        },
        cancelDelConv(idx, conv) {
            conv.delete = false;
            var that = this
            that.$set(that.conversations, idx, conv);
        },
        loadAvatar() {
            var avatar = localStorage.getItem("avatar") || Math.ceil(Math.random() * 9);
            this.avatarIdx = avatar;
        },
        handleScrollBottom() {
            this.$nextTick(() => {
                let scrollElem = this.$refs.chatContainer;
                scrollElem.scrollTo({top: scrollElem.scrollHeight, behavior: 'smooth'});
            });
        },
        isScrollAndNotBottom() {
            let chatDivEle = this.$refs.chatContainer;
            if (!chatDivEle) {
                return;
            }

            if (chatDivEle.scrollHeight <= chatDivEle.clientHeight) {
                this.isShowGoBottom = false;
                return;
            }

            const scrollTop = chatDivEle.scrollTop;
            const windowHeight = chatDivEle.clientHeight;
            const scrollHeight = chatDivEle.scrollHeight;
            if (scrollTop + windowHeight >= scrollHeight - 50) {
                this.isShowGoBottom = false;
                return;
            }

            this.isShowGoBottom = true;
        },
        closeEduEmail() {
            document.getElementById("wefive-a-check").style.display = "none";
            this.chooseone();
            // document.getElementById("model-content-choose").style.display = "flex";
        },
        checkemial() {
            // 隐藏套餐菜单
            this.is_erro_msg = false;
            this.is_msg = false;
            document.getElementById("model-content-choose").style.display = "none";
            const modal1 = document.getElementById("wefive-a-check");
            modal1.style.display = "flex";
            // var checkEmailFunc = function (event) {
            //     const modal1 = document.getElementById("wefive-a-check");
            //     if (event.target !== modal1) {
            //         modal1.style.display = "none";
            //         document.removeEventListener('click', checkEmailFunc);
            //     }
            // }
            // document.addEventListener('click', checkEmailFunc);
            // // // console.log('done!')
        },
        // 用户登录弹窗
        // 加载图片信息
        showimg() {
            var that = this;
            this.axios.post("https://api.tpcosmo.com/QrLogin").then(function (response) {
                var respon = response.data
                that.code_login = respon.code
                if (respon.code === 200) {
                    // document.getElementById('we1').src = 'data:image/jpg;base64,' + respon.qr_url;
                    document.getElementById('we1').src = respon.qr_url;
                    document.getElementById('load-login').style.display = "none";
                    document.getElementById('we1').style.display = "flex";
                    that.login_id = respon.login_id;
                    that.is_load_to_login = false;
                    that.loopAsk()
                }
            })
        },

        loopAsk() {
            var that = this
            that.t1 = setInterval(function () {
                that.t2 = setTimeout(function () {
                    that.askLoginInfo()
                }, 1000)
            }, 1000)
        },
        askLoginInfo() {
            if (localStorage.getItem('token')) {
                location.reload();
            }
            var that = this;
            var wei = document.getElementById('we1')
            this.axios.get("https://api.tpcosmo.com/QrLogin/" + this.login_id).then(function (respn) {
                var responsee = respn.data;
                that.code = responsee.code;
                if (responsee.code === 200) {
                    that.token_msg = responsee.token
                    localStorage.setItem('token', responsee.token);
                    location.reload();
                    // 更新chat id
                    // that.loadId();
                    this.getSidebarTitles();
                    clearInterval(that.t1);
                    clearInterval(that.t2);
                    // document.getElementById("we1").empty();
                    document.getElementById('show-login').style.display = "none";
                } else if (responsee.code === 403) {
                    alert(responsee.msg);
                } else if (responsee.code === 404) {
                }
            })
        },
        history_func() {
            var that = this;
            if (window.innerWidth < 1048) {
                that.closeShowSlide();
            }
        },
        newChat() {

            // console.log('new chat!')
            this.is_new_chat = true;

            // console.log('this.is_new_chat:', this.is_new_chat)
            this.closeShowSlide();
            if (this.conversation.length === 0) {
                return null;
            }
            this.chatTitle = "New chat";
            // document.title = "New chat";
            this.conversation = [];
            var conversations = this.conversations;
            for (let idx in conversations) {
                var conv = conversations[idx];
                delete conv.editable;
                delete conv.selected;
                delete conv.delete;
            }
        },
        // 执行弹窗在send那里添加
        showLoginModal() {
            const buttonsend = document.getElementById("tanchuang");
            const modalsend = document.getElementById("show-login");
            var that = this;
            that.showimg();
            modalsend.style.display = "block";
        },
        jugelogin() {
            var that = this
            // 检测本地token
            var token = localStorage.getItem('token');
            if (!token) {
                this.showLoginModal();
                return null;
            }
            this.axios.get("https://api.tpcosmo.com/user_data", {
                headers: {
                    "token": token,
                }
            }).then(function (respn) {
                // that.is_load_to_login = true;
                var responsee = respn.data
                if (responsee.code === 200) {
                    // that.code = responsee.code
                    that.user_data = respn.data.data
                    // that.is_load_to_login = false;
                    return false;
                } else if (responsee.code === 403) {
                    that.showLoginModal();
                    return true
                }
            });
        },
        // 订阅前先登录判断弹窗
        // 订阅前先choose
        chooseone() {
            var that = this;
            this.wechat_is_active = false;
            this.alipay_is_active = false;
            const modal5 = document.getElementById("choose");
            document.getElementById("model-content-choose").style.display = "";
            modal5.style.display = "block";
            //   点击其他领域(即弹窗背景)
            var chooseFunc = function (event) {
                // // // console.log('click:', event.target)
                if (event.target === modal5) {
                    modal5.style.display = "none";
                    document.removeEventListener('click', chooseFunc);
                }
            }
            document.addEventListener('click', chooseFunc);
            if (window.innerWidth < 1048) {
                that.closeShowSlide()
            }
        },
        reChooseOne() {
            var that = this
            this.wechat_is_active = false;
            this.alipay_is_active = false;
            // 隐藏元素
            document.getElementById("casher").style.display = 'none';

            // start
            const button5 = document.getElementById("payfor");
            const modal5 = document.getElementById("choose");
            modal5.style.display = "block";
            //   点击其他领域(即弹窗背景)
            var chooseFunc = function (event) {
                // // // console.log('click:', event.target)
                if (event.target === modal5) {
                    modal5.style.display = "none";
                    document.removeEventListener('click', chooseFunc);
                }
            }
            document.addEventListener('click', chooseFunc);
            if (window.innerWidth < 1048) {
                that.closeShowSlide()
            }
        },
        upgrade(upgrade_scheme_describe, upgrade_scheme_amount) {
            this.pay_erro = false;
            // // // console.log(this.user_data)
            // // // // console.log("user_data:", this.user_data)
            // 判断是否需要进行教育认证
            if (upgrade_scheme_describe === "教育优惠" && !this.user_data.is_edu) {
                // alert("您还未进行教育认证,该功能即将上线!")
                // // // console.log("请先完成认证!")
                this.checkemial()
                return null;
            }
            // 隐藏收银台
            document.getElementsByClassName("model2-content")[0].style.display = "none";
            const el = document.getElementsByClassName("model1-content")[0];
            // // // console.log(el)
            el.style.display = "flex";
            var that = this;
            this.upgrade_scheme_describe = upgrade_scheme_describe
            this.upgrade_scheme_amount = upgrade_scheme_amount
            // 取消选择弹框
            document.getElementById("choose").style.display = "none";
            // document.removeEventListener('click', chooseFunc);

            const buttonedu = document.getElementById("edu-check");
            const modaledu = document.getElementById("casher");
            modaledu.style.display = "block";
            var payforeduFunc = function (event) {
                if (event.target === modaledu) {
                    modaledu.style.display = "none";
                    document.removeEventListener('click', payforeduFunc);
                }
            }
            document.addEventListener('click', payforeduFunc);
        },
        showpaylianjie(connection) {
            window.open(connection, '_blank');
        },
        normalpayfor1img() {
            var that = this
            var token = localStorage.getItem("token")
            this.axios.post("https://api.tpcosmo.com/enrol", {
                "fellow_type": "VIP",
                "platform": "wechat"
            }, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"

                }
            }).then(function (response) {
                var respon = response.data
                if (respon.code === 200) {
                    // document.getElementById('we1').src = 'data:image/jpg;base64,' + respon.qr_url;
                    document.getElementById('we-wechat').src = 'data:image/jpg;base64,' + respon.pay_qr;
                    document.getElementById('money-wechat').innerHTML = respon.total_amount;
                    that.pay_id = respon.pay_id
                    that.loopAsk1()
                } else if (respon.code === 403) {
                    alert(respon.msg)
                }
            })
        },
        loopAsk1() {
            var that = this
            that.t1 = setInterval(function () {
                that.t2 = setTimeout(function () {
                    that.askLoginInfo1()
                }, 2000)
            }, 2000)
        },
        askLoginInfo1() {
            var token = localStorage.getItem("token")
            var that = this
            this.axios.get("https://api.tpcosmo.com/check_pay/" + this.pay_id, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"
                }
            }).then(function (respn) {
                var responsee = respn.data
                that.code = responsee.code
                if (responsee.code === 200) {
                    that.token_msg = responsee.token
                    clearInterval(that.t1)
                    clearInterval(that.t2)
                    alert('支付成功！')
                    document.getElementById('wxin').style.display = "none";
                    document.getElementById('modelwec-normal').style.display = "none";
                } else if (responsee.code === 403) {
                    alert(responsee.msg)
                } else if (responsee.code === 404) {
                    alert(responsee.msg)
                }

            })
        },
        payForIt() {
            var that = this;
            if (!this.wechat_is_active && !this.alipay_is_active) {
                this.pay_erro = true;
                return null
            }
            this.pay_erro = false;
            that.is_loading_qr_img = false;

            // 隐藏收银台
            document.getElementsByClassName("model1-content")[0].style.display = "none";
            // 显示付款
            document.getElementsByClassName("model2-content")[0].style.display = "flex";
            // 显示加载动画
            document.getElementsByClassName('qr-img')[0].src = "./src/assets/imgs/loading.svg";

            // 请求获取qr img
            var token = localStorage.getItem("token")
            let fellow_type = ""
            if (this.upgrade_scheme_describe === "教育优惠") {
                fellow_type = "edu_VIP";
            } else if (this.upgrade_scheme_describe === "标准会员") {
                fellow_type = "VIP";
            } else if (this.upgrade_scheme_describe === "专业会员") {
                fellow_type = "Professional";
            }

            // WeChat Pay
            if (this.wechat_is_active) {
                // alert(this.isWeChatBrowser);
                // qr code
                if (!this.isWeChatBrowser) {
                    this.axios.post("https://api.tpcosmo.com/enrol", {
                        "fellow_type": fellow_type,
                        "platform": "wechat"
                    }, {
                        headers: {
                            "token": token,
                            "Content-Type": "application/json"
                        }
                    }).then(function (response) {
                        // 处理返回结果
                        var respon = response.data
                        alert('返回结果: ', respon)
                        if (respon.code === 200) {

                            that.is_loading_qr_img = true;
                            document.getElementsByClassName('qr-img')[0].src = 'data:image/jpg;base64,' + respon.pay_qr;
                            that.pay_id = respon.pay_id
                            that.loopAsk3()
                        } else if (respon.code === 403) {
                            alert(respon.msg)
                        }
                    });
                } else { // WeChat JSAPI
                    alert("即将调用微信支付,请勿离开此界面！");
                    // 调用微信支付
                    // {'result': {'appId': 'wxe59bf8bfee088d72', 'timeStamp': '1691030127446', 'nonceStr': 'BZJoRZo', 'package': 'prepay_id=wx031035273659449afd81132b1382dd0000', 'signType': 'RSA', 'paySign': 'QeSK4BBzq5wEgXDGsz+KLlsqec3qhZnhf3MpoJA14k3M2iBCs7kEVoCtLqN4oCHNRG/Ka1uoSLO+PLQ44uYAeV8sLU613LscYiHwYk9ONidsHtJ9hVUjd5Jga/dybSM3Smao/WogznhVlBvqIdg+h14u1uR5lNXCr2plw9iuc9pkUtF/7fSlgF3WP9XthNKNjYlOOPcMWcgxCErkRnuXDPhgrK7rNLaRzGhIi6UnG2CzIQTH5DsfKy6pwbxIeD8sQNx7OuFUXmjXKcc85hS3wfF3HMrcwx7HxeXR3WgQELYEKu6ayM4NOieQ0mXjImWeAKdJbghdtoGANDBHj5pXxw=='}}
                    // 替换成您自己的微信公众号或小程序的AppID
                    // alert("ready to request");
                    this.axios.post("https://api.tpcosmo.com/enrol", {
                        "fellow_type": fellow_type,
                        "platform": "wechat1"
                    }, {
                        headers: {
                            "token": token,
                            "Content-Type": "application/json"
                        }
                    }).then(function (response) {
                        // alert("handle result");
                        // 处理返回结果
                        var respon = response.data;
                        // alert(response.toString());
                        // alert(respon.toString());
                        if (respon.code === 200) {
                            that.is_loading_qr_img = true;
                            // var appid = 'wxe59bf8bfee088d72';
                            // 替换成您的预支付交易会话标识（prepay_id）
                            // var prepayId = 'wx02115223170178af9014cff8c1d9ff0000';

                            // 使用微信JSAPI调起支付
                            function onBridgeReady() {
                                WeixinJSBridge.invoke('getBrandWCPayRequest', {
                                    "appId": respon.result.appId,     // 公众号或小程序的AppID
                                    "timeStamp": respon.result.timeStamp,    // 时间戳，由后台生成
                                    "nonceStr": respon.result.nonceStr,     // 随机字符串，由后台生成
                                    "package": respon.result.package,      // 统一下单接口返回的 package 值
                                    "signType": respon.result.signType,  // 签名类型，默认为MD5
                                    "paySign": respon.result.paySign,      // 支付签名，由后台生成
                                }, function (res) {
                                    // alert(res)
                                    if (res.err_msg == "get_brand_wcpay_request:ok") {
                                        // 支付成功的回调
                                        alert("支付成功！");
                                        location.reload();
                                    } else {
                                        // 支付失败的回调
                                        alert("支付失败，请稍后重试！");
                                        location.reload();
                                    }
                                    that.is_loading_qr_img = false;
                                });
                            }

                            onBridgeReady();
                        } else {
                            alert(respon.result.reason)
                        }
                    });

// 注册微信JSAPI支付的回调函数
                    function callPay() {
                        if (typeof WeixinJSBridge == "undefined") {
                            if (document.addEventListener) {
                                document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
                            } else if (document.attachEvent) {
                                document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
                                document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
                            }
                        } else {
                            onBridgeReady();
                        }
                    }

                    callPay();
                    alert("callPay done!");

                }

            }
            // AliPay
            if (this.alipay_is_active) {
                // this.wechat_is_active = false;
                // this.alipay_is_active = false;
                this.axios.post("https://api.tpcosmo.com/enrol", {
                    "fellow_type": fellow_type,
                    "platform": "alipay"
                }, {
                    headers: {
                        "token": token,
                        "Content-Type": "application/json"
                    }
                }).then(function (response) {
                    // 处理返回结果
                    var respon = response.data
                    if (respon.code === 200) {
                        // that.is_loading_qr_img = true;
                        alert("即将跳转支付页面!")
                        location.href = respon.pay_url;
                        // document.getElementsByClassName('qr-img')[0].src = 'data:image/jpg;base64,' + respon.pay_qr;
                        // that.pay_id = respon.pay_id
                        // that.loopAsk3()
                        // location.reload()
                        // setTimeout(function () {
                        //     location.reload();
                        // }, 500)
                    } else if (respon.code === 403) {
                        alert(respon.msg)
                    }
                });
            }
        },
        eduimg() {
            var that = this
            var token = localStorage.getItem("token")
            this.axios.post("https://api.tpcosmo.com/enrol", {
                "fellow_type": "edu_VIP",
                "platform": "wechat"
            }, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"
                }
            }).then(function (response) {
                var respon = response.data
                if (respon.code === 200) {
                    // document.getElementById('we1').src = 'data:image/jpg;base64,' + respon.qr_url;
                    document.getElementById('we-wechat').src = 'data:image/jpg;base64,' + respon.pay_qr;
                    document.getElementById('money-wechat').innerHTML = respon.total_amount;
                    that.pay_id = respon.pay_id
                    that.loopAsk2()
                } else if (respon.code === 403) {
                    document.getElementById("wxin").style.display = 'none';
                    alert(respon.msg)
                }
            })
        },
        loopAsk2() {
            var that = this
            that.t1 = setInterval(function () {
                that.t2 = setTimeout(function () {
                    that.eduLoginInfo1()
                }, 2000)
            }, 2000)
        },
        eduLoginInfo1() {
            var token = localStorage.getItem("token")
            var that = this
            this.axios.get("https://api.tpcosmo.com/check_pay/" + this.pay_id, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"
                }
            }).then(function (respn) {
                var responsee = respn.data
                that.code = responsee.code
                if (responsee.code === 200) {
                    that.token_msg = responsee.token
                    clearInterval(that.t1)
                    clearInterval(that.t2)
                    alert('支付成功！')
                    document.getElementById('wxin').style.display = "none";
                    document.getElementById('casher').style.display = "none";
                } else if (responsee.code === 403) {
                    alert(responsee.msg)
                } else if (responsee.code === 404) {
                    alert(responsee.msg)
                }

            })
        },
        superimg() {
            var that = this
            var token = localStorage.getItem("token")
            this.axios.post("https://api.tpcosmo.com/enrol", {
                "fellow_type": "Professional",
                "platform": "wechat"
            }, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"

                }
            }).then(function (response) {
                var respon = response.data
                if (respon.code === 200) {
                    // document.getElementById('we1').src = 'data:image/jpg;base64,' + respon.qr_url;
                    document.getElementById('we-wechat').src = 'data:image/jpg;base64,' + respon.pay_qr;
                    document.getElementById('money-wechat').innerHTML = respon.total_amount;
                    that.pay_id = respon.pay_id
                    that.loopAsk3()
                } else if (respon.code === 403) {
                    alert(respon.msg)
                }
            })
        },
        loopAsk3() {
            var that = this
            that.t1 = setInterval(function () {
                that.t2 = setTimeout(function () {
                    that.eduLoginInfo3()
                }, 5000)
            }, 5000)
        },
        eduLoginInfo3() {
            var token = localStorage.getItem("token")
            var that = this
            this.axios.get("https://api.tpcosmo.com/check_pay/" + this.pay_id, {
                headers: {
                    "token": token,
                    "Content-Type": "application/json"
                }
            }).then(function (respn) {
                var responsee = respn.data
                that.code = responsee.code
                if (responsee.code === 200) {
                    that.token_msg = responsee.token
                    clearInterval(that.t1)
                    clearInterval(that.t2)
                    location.reload()
                    alert('支付成功！')
                    document.getElementById('wxin').style.display = "none";
                    document.getElementById('modelwec-super').style.display = "none";
                } else if (responsee.code === 403) {
                    alert(responsee.msg)
                } else if (responsee.code === 404) {
                    alert(responsee.msg)
                }

            })
        },
        // 邮箱验证
        sendCode() {
            var that = this
            this.is_erro_msg = false;
            this.is_msg;
            var token = localStorage.getItem("token")
            var email = document.getElementById("input-email").value;
            var regex = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            if (!email) {
                that.is_erro_msg = true;
                that.erro_msg = "请输入邮箱 !"
                return null;
            }
            if (regex.test(email)) {
                if (email.endsWith(".edu.cn" || ".edu")) {
                    that.settime(60)
                    this.axios.post("https://api.tpcosmo.com/edu_code", {
                        "email": email
                    }, {
                        headers: {
                            // "token": this.$store.state.token
                            "token": token,
                            "Content-Type": 'application/json'
                        }
                    }).then(function (response) {
                        var dt = response.data
                        if (dt.code === 200) {
                            that.is_erro_msg = false
                            that.is_msg = true;
                            that.msg = "验证码已发送，请注意查收！";
                        } else {
                            that.is_erro_msg = true;
                            that.erro_msg = dt.msg;
                            that.settime(0)
                            return false
                        }
                    })
                } else {
                    that.is_erro_msg = true;
                    that.erro_msg = "输入教育邮箱格式有误 !";
                    return false
                }
            } else {
                that.is_erro_msg = true;
                that.erro_msg = "输入教育邮箱格式有误 !";
                return false;
            }
        },
        // 提交验证
        checksub() {

            var that = this;
            this.is_erro_msg = false;
            this.is_msg = false;
            var btnSendCode = document.getElementById("btn-test");
            var email = document.getElementById("input-email").value;
            var testcode = document.getElementById("input-test").value;
            var testcode1 = document.getElementById("wefive-a-check")
            var token = localStorage.getItem("token");
            if (email) {
                const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

                // 使用正则表达式测试输入是否符合邮箱格式
                if (!emailPattern.test(email)) {
                    this.is_erro_msg = true;
                    this.erro_msg = "邮箱格式有误,请重试!";
                    return null;
                }

                if (!testcode) {
                    that.is_erro_msg = true;
                    that.erro_msg = "请输入验证码 !";
                    return null;
                }
                this.request_is_loading = true;
                that.axios.post("https://api.tpcosmo.com/edu_auth", {
                    "email": email,
                    "code": testcode
                }, {
                    headers: {
                        "token": token,
                        "Content-Type": 'application/json'
                    }
                }).then(function (response) {
                    var respnses = response.data
                    that.request_is_loading = false;

                    if (respnses.code === 200) {
                        alert(respnses.msg);
                        // document.getElementById("input-email").value = "";
                        // document.getElementById("input-test").value = "";
                        testcode1.style.display = 'none';
                        location.reload();
                    } else {
                        alert(respnses.msg);
                        // document.getElementById("input-test").value = "";
                        that.request_is_loading = false;
                        // return false
                    }
                });
                // 验证码倒计时
                // var a = 60;
                // while (a >= 1) {
                //     document.getElementById("btn-test").value = a + "s后重试"
                // }

            } else {
                that.erro_msg = "请输入邮箱 !";
                that.is_erro_msg = true;
                that.request_is_loading = false;
                return false;
            }
        },
        choseAliPay() {
            this.pay_erro = false;
            // // // // console.log('chose alipay...')
            this.alipay_is_active = true
            this.wechat_is_active = false;
        },
        choseWechatPay() {
            this.pay_erro = false;
            // // // // console.log('chose wechat...')
            this.alipay_is_active = false;
            this.wechat_is_active = true;
        },
        //   反馈
        feedback() {
            var that = this
            const button3 = document.getElementById("feedback1");
            const modal3 = document.getElementById("fed");
            modal3.style.display = "block";
            var feedbackFunc = function (event) {
                if (event.target === modal3) {
                    modal3.style.display = "none";
                    document.removeEventListener('click', feedbackFunc);
                }
            }
            document.addEventListener('click', feedbackFunc);
            if (window.innerWidth < 1048) {
                that.closeShowSlide()
            }
        },
        subfedback() {
            var text = document.getElementById("fed-text").value;
            var text1 = document.getElementById("fed")
            if (!text) {
                alert("请输入反馈内容！")
                return false
            } else {
                text1.style.display = 'none'

                this.axios.post("https://api.tpcosmo.com/feedback", {
                    "content": text,
                    "contact": ""
                }).then(function (response) {
                    var res = response.data
                    if (res.code === 200) {
                        alert("反馈成功！")
                        document.getElementById('fed-text').value = null;
                    } else {
                        alert("反馈失败！请稍后重试！")

                        return false
                    }
                })
            }
        },
        // 验证码倒计时
        settime(time) {
            var btnSendCode = document.getElementById("btn-test");
            // // // console.log("倒计时开始...")
            if (time === 0) {
                // btnSendCode.disabled=false
                btnSendCode.removeAttribute("disabled")
                btnSendCode.innerText = "获取验证码";
                return;
            } else if (time > 0) {
                btnSendCode.setAttribute("disabled", true);
                btnSendCode.innerText = time + "秒后获取";
                time--;
            }
            var that = this
            setTimeout(function () {
                that.settime(time);
            }, 1000);
        },
        logout() {
            var that = this
            var a = confirm("确定退出?"); //在页面上弹出对话框
            if (a === true) {
                localStorage.removeItem("token");
                location.reload()
            } else {
            }
            if (window.innerWidth < 1048) {
                that.closeShowSlide()
            }
        }
    },
    computed: {},
    watch: {
        chatMsg(newVal, oldVal) {
            if (newVal === oldVal) {
                return;
            }
            this.changeHeight();
        }
    },
    mounted: function () {
        // this.fetchMessages();
        let index = Math.round(Math.random() * 3);
        this.pic = this.imgs[index];
        var theme = localStorage.getItem("theme") || "light";
        this.JudgeWechatBrowser();
        this.changeTheme(theme);
        this.newChat();
        // this.loadConversations();
        // this.clearConversations();
        this.jugelogin();
        // this.loadId();
        this.getSidebarTitles();
        this.loadAvatar();
        let chatDivEle = this.$refs.chatContainer;
        chatDivEle.addEventListener('scroll', this.isScrollAndNotBottom, true)
        window.copy = this.vueCopy;
        // this.jugelogin()
        chatDivEle.addEventListener('scroll', this.isScrollAndNottop, true)
    },
};
</script>
<style lang="scss">

html, body, #app {
    margin: 0;
    padding: 0;
    height: 100%;
}

.flex_row_c_c {
    display: flex;
    align-content: center;
    flex-direction: row;
    justify-items: center;
}

.react-scroll-to-bottom--css-krija-1n7m0yu {
    height: 100%;
    overflow-y: auto;
    width: 100%;
}

.code_header {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

.prose :where(code):not(:where([class~=not-prose] *)):before {
    content: "" !important;
}

.prose :where(code):not(:where([class~=not-prose] *)):after {
    content: "" !important;
}

#chatRepeat:focus {
    --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
    --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    --tw-ring-offset-width: 0px;
    box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), 0 0 transparent;
    //box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 transparent);
}

.suitable_selected {
    --tw-text-opacity: 1 !important;
    cursor: auto !important;
}

.load_dot1 {
    -webkit-animation: blink 1s steps(2, start) infinite;
    animation: blink 1s steps(2, start) infinite;
}

.load_dot2 {
    -webkit-animation: blink 1s steps(3, start) infinite;
    animation: blink 1s steps(3, start) infinite;
}

.load_dot3 {
    -webkit-animation: blink 1s steps(4, start) infinite;
    animation: blink 1s steps(4, start) infinite;
}

#app .markdown h1 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

#app .markdown h2 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

#app .markdown h3 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

#app .markdown h4 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

#app .markdown h5 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

#app .markdown h6 {
    margin-bottom: 0rem;
    margin-top: 0rem;
}

@media (max-width: 640px) {
    #app .none {
        display: none;
    }
}

.w-180px {
    width: 180px;
}

.prose-r {
    font-size: 1rem;
    line-height: 1.75;
}

.markdown pre {
    @apply bg-[#282c34] p-4 mt-4 rounded-md text-white w-full overflow-x-auto;
}

.markdown code {
    width: 100%;
}

/** 控制段落间的上下边距 **/
.markdown p {
    margin: 1.25rem 0;
}

.markdown p:first-child {
    margin-top: 0;
}

/** 小代码块样式，对应 markdown 的 `code` **/
.markdown :not(pre) > code {
    @apply bg-[#282c34] px-1 py-[2px] text-[#e06c75] rounded-md;
}

/** 列表样式 **/
.markdown ol {
    list-style-type: decimal;
    padding-left: 40px;
}

.markdown ul {
    list-style-type: disc;
    padding-left: 40px;
}

/** 光标样式 **/
.markdown .cursor {
    display: inline-block;
    width: 2px;
    height: 20px;
    @apply bg-gray-800 dark:bg-gray-100;
    animation: blink 1.2s step-end infinite;
    margin-left: 2px;
    vertical-align: sub;
}

@keyframes blink {
    0% {
        opacity: 1;
    }
    50% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

</style>
