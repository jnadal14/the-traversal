/**
 * Gallery order. This file is the only place the mosaic's contents are defined —
 * edit it to add, remove or reorder work.
 *
 *   image('assets/photos/name.jpg', width, height)
 *   video('assets/video/name.mp4', width, height)
 *
 * The width and height are the file's real pixel dimensions. They reserve each
 * tile at the correct shape before its media loads, so the masonry never shifts
 * under the reader while they scroll. Get them with:
 *
 *   sips -g pixelWidth -g pixelHeight assets/photos/name.jpg
 *
 * Adding new work:
 *   1. Drop the originals in _masters/photos/ or _masters/video/ (git-ignored).
 *   2. python3 scripts/optimize-photos.py     — writes assets/photos/
 *      ./scripts/encode-video.sh              — writes assets/video/ + posters
 *   3. Add a line below and bump ASSET_VERSION.
 *
 * Vertical clips stay vertical: pass their real dimensions and they occupy a tall
 * tile in the masonry instead of being cropped to a letterbox.
 */
window.GALLERY_MANIFEST = (() => {
    // Bump whenever a file under assets/ is replaced, so browsers refetch.
    const ASSET_VERSION = '20260827';
    const v = (src) => `${src}?v=${ASSET_VERSION}`;

    const image = (src, width, height, alt) => ({ type: 'image', src: v(src), width, height, alt });

    // Poster path mirrors the clip's own name, written by scripts/encode-video.sh.
    const video = (src, width = 16, height = 9) => ({
        type: 'video',
        src: v(src),
        poster: v(src.replace('assets/video/', 'assets/posters/').replace(/\.mp4$/i, '.jpg')),
        width,
        height,
    });

    return [
        image('assets/photos/bar-tartare.jpg', 2200, 1458),
        image('assets/photos/01.jpg', 2000, 2500),
        image('assets/photos/ellipsis-heart.jpg', 2200, 1467),
        image('assets/photos/gold-030.jpg', 2200, 1470),
        image('assets/photos/kodakpro-009.jpg', 2200, 1470),
        video('assets/video/abott-2.mp4', 1920, 1080),
        image('assets/photos/gc-026.jpg', 1470, 2200),
        image('assets/photos/16.jpg', 2000, 1325),
        image('assets/photos/32.jpg', 1760, 2200),
        image('assets/photos/03.jpg', 2000, 1325),
        image('assets/photos/portra-026.jpg', 1760, 2200),
        video('assets/video/saskatchewan-1.mp4', 1920, 1080),
        image('assets/photos/15.jpg', 1760, 2200),
        image('assets/photos/10.jpg', 2000, 1124),
        image('assets/photos/31.jpg', 1760, 2200),
        image('assets/photos/gc-013.jpg', 2200, 1470),
        image('assets/photos/gc-003.jpg', 2200, 1470),
        video('assets/video/icefields-2.mp4', 1920, 1080),
        image('assets/photos/18.jpg', 1760, 2200),
        image('assets/photos/02.jpg', 2000, 1124),
        image('assets/photos/gold-032.jpg', 2200, 1470),
        image('assets/photos/08.jpg', 1760, 2200),
        video('assets/video/fire-lookout-1.mp4', 1920, 1080),
        image('assets/photos/gold-051.jpg', 1470, 2200),
        image('assets/photos/man-under-snowy-mountain.jpg', 2200, 1458),
        image('assets/photos/05.jpg', 1760, 2200),
        image('assets/photos/04.jpg', 2000, 1325),
        video('assets/video/saskatchewan-2.mp4', 1920, 1080),
        image('assets/photos/cinestill400d-030.jpg', 1760, 2200),
        image('assets/photos/22.jpg', 2000, 1325),
        image('assets/photos/cinestill400d-039.jpg', 2087, 2200),
        image('assets/photos/neon-cola.jpg', 2200, 1459),
        image('assets/photos/23.jpg', 1760, 2200),
        video('assets/video/awaga-1.mp4', 1920, 1080),
        image('assets/photos/gold-029.jpg', 2200, 1470),
        image('assets/photos/gold-021.jpg', 1470, 2200),
        image('assets/photos/25.jpg', 2000, 1325),
        image('assets/photos/ellipsis-light.jpg', 1760, 2200),
        image('assets/photos/ellipsis-room.jpg', 2200, 1458),
        image('assets/photos/kodakpro-017.jpg', 1470, 2200),
        image('assets/photos/30.jpg', 2000, 1325),
        video('assets/video/abott-1.mp4', 1920, 1080),
        image('assets/photos/portra-036.jpg', 2200, 1470),
        image('assets/photos/21.jpg', 1760, 2200),
        image('assets/photos/28.jpg', 2000, 1325),
        image('assets/photos/portra-006.jpg', 1469, 2200),
        image('assets/photos/11.jpg', 2000, 1325),
        image('assets/photos/26.jpg', 2000, 1325),
        video('assets/video/garibaldi.mp4', 1080, 1920),
        image('assets/photos/13.jpg', 2000, 1325),
        image('assets/photos/portra-012.jpg', 2200, 1470),
        image('assets/photos/cass-and-aiden.jpg', 2200, 1458),
        image('assets/photos/cinestill400d-037.jpg', 1470, 2200),
        image('assets/photos/14.jpg', 2000, 1325),
        video('assets/video/pacific-spirit.mp4', 1080, 1920),
        image('assets/photos/19.jpg', 2000, 1325),
        image('assets/photos/29.jpg', 2000, 1325),
        image('assets/photos/24.jpg', 2000, 1325),
        image('assets/photos/33.jpg', 1760, 2200),
        image('assets/photos/portra-008.jpg', 2200, 1470),
        image('assets/photos/12.jpg', 2000, 1325),
        video('assets/video/fire-lookout-2.mp4', 1920, 1080),
        image('assets/photos/27.jpg', 1760, 2200),
        image('assets/photos/gold-015.jpg', 2200, 1470),
        image('assets/photos/ellipsis-corner.jpg', 1458, 2200),
        image('assets/photos/ethan-and-roman.jpg', 2200, 1458),
        image('assets/photos/06.jpg', 2000, 1325),
        image('assets/photos/kodakpro-028.jpg', 1470, 2200),
        video('assets/video/icefields-1.mp4', 1920, 1080),
        image('assets/photos/07.jpg', 2000, 1325),
    ];
})();
