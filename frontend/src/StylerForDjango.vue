<!-- This is a horendous hack to make styles available to Django templates, until I find a way of getting Vite to see those templates directly -->
<template>
    <div>
        <div class="navbar bg-base-100 shadow-sm flex-1 btn btn-ghost text-xl flex-none menu menu-horizontal px-1 no-underline container max-w-4xl mx-auto px-4 mt-6">
            BASE
        </div>

        <div class="text-center text-base-content divider mt-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 card card-sm border border-gray-700 w-full h-40 object-cover rounded-t-lg card-body card-title text-lg font-semibold flex items-center gap-3 mt-3 btn btn-primary cursor-pointer relative absolute top-2 right-2 badge badge-primary badge-outline badge-info badge-soft badge-secondary">
            PROMPTS
        </div>

        <div class="text-center text-4xl font-bold text-base-content my-4 youtube-embed mt-8">
            INDEX
        </div>

        <div class="flex justify-center items-center h-screen card w-96 bg-base-100 shadow-xl p-6 text-2xl font-bold text-center mb-4 space-y-4 form-control label label-text input input-bordered w-full text-red-500 text-sm mt-1 btn btn-primary w-full text-center text-sm mt-4 text-blue-500">
            REGISTER
        </div>

        <div class="hero bg-base-200 min-h-[50vh] hero-content text-center max-w-md text-5xl font-bold py-6">
            HOME
        </div>
    </div>
</template>