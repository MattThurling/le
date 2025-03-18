<!-- This is a horendous hack to make styles available to Django templates, until I find a way of getting Vite to see those templates directly -->
<template>
    <div>
        <div class="navbar bg-base-100 shadow-sm flex-1 btn btn-ghost text-xl flex-none menu menu-horizontal px-1 no-underline container max-w-4xl mx-auto px-4 mt-6">
            BASE
        </div>

        <div class="text-center text-base-content divider mt-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 card card-sm border border-gray-700 w-full h-40 object-cover rounded-t-lg card-body card-title text-lg font-semibold flex items-center gap-3 mt-3 btn btn-primary cursor-pointer">
            PROMPTS
        </div>

        <div class="text-center text-4xl font-bold text-base-content my-4 youtube-embed mt-8">
            INDEX
        </div>
    </div>
</template>