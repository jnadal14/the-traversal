/**
 * Gallery order. This file is the only place the mosaic's contents are defined —
 * edit it to add, remove or reorder work.
 *
 *   image('assets/photos/name.jpg', width, height, '#tint')
 *   video('assets/video/name.mp4', width, height, '#tint')
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

    // `tint` is the photograph's own mean colour. The tile is painted with it
    // before the media arrives, so a slow connection shows the picture's colour
    // rather than a white hole, and the image fades in over its own average.
    // scripts/curate-order.py measures it.
    const image = (src, width, height, tint, alt) =>
        ({ type: 'image', src: v(src), width, height, tint, alt });

    // Poster path mirrors the clip's own name, written by scripts/encode-video.sh.
    const video = (src, width = 16, height = 9, tint) => ({
        type: 'video',
        src: v(src),
        poster: v(src.replace('assets/video/', 'assets/posters/').replace(/\.mp4$/i, '.jpg')),
        width,
        height,
        tint,
    });

    return [
        image('assets/photos/bar-tartare.jpg', 2200, 1458, '#2f0a06'),
        video('assets/video/garibaldi.mp4', 1080, 1920, '#3c442f'),
        image('assets/photos/portra-012.jpg', 2200, 1470, '#7b7c79'),
        image('assets/photos/kodakpro-028.jpg', 1470, 2200, '#201b11'),
        image('assets/photos/ellipsis-room.jpg', 2200, 1458, '#6c807f'),
        image('assets/photos/ethan-and-roman.jpg', 2200, 1458, '#4d4028'),
        image('assets/photos/08.jpg', 1760, 2200, '#4c5d5e'),
        video('assets/video/fire-lookout-1.mp4', 1920, 1080, '#5c4740'),
        image('assets/photos/19.jpg', 2000, 1325, '#736e4a'),
        image('assets/photos/gc-013.jpg', 2200, 1470, '#443738'),
        image('assets/photos/gc-003.jpg', 2200, 1470, '#68715d'),
        video('assets/video/awaga-1.mp4', 1920, 1080, '#5f3e3a'),
        image('assets/photos/07.jpg', 2000, 1325, '#5d563c'),
        image('assets/photos/03.jpg', 2000, 1325, '#5e6e72'),
        image('assets/photos/gc-026.jpg', 1470, 2200, '#3f3b28'),
        image('assets/photos/24.jpg', 2000, 1325, '#57554f'),
        video('assets/video/pacific-spirit.mp4', 1080, 1920, '#2e2b29'),
        image('assets/photos/02.jpg', 2000, 1124, '#60858f'),
        image('assets/photos/13.jpg', 2000, 1325, '#5c4842'),
        image('assets/photos/01.jpg', 2000, 2500, '#696f6c'),
        image('assets/photos/ellipsis-heart.jpg', 2200, 1467, '#4d1c07'),
        image('assets/photos/portra-036.jpg', 2200, 1470, '#686457'),
        video('assets/video/abott-1.mp4', 1920, 1080, '#3e404e'),
        image('assets/photos/gold-015.jpg', 2200, 1470, '#533e21'),
        image('assets/photos/16.jpg', 2000, 1325, '#6f6b62'),
        image('assets/photos/cass-and-aiden.jpg', 2200, 1458, '#1c362e'),
        image('assets/photos/10.jpg', 2000, 1124, '#6a6e6d'),
        image('assets/photos/gold-021.jpg', 1470, 2200, '#573e10'),
        video('assets/video/abott-2.mp4', 1920, 1080, '#574e61'),
        image('assets/photos/32.jpg', 1760, 2200, '#392b10'),
        image('assets/photos/25.jpg', 2000, 1325, '#738685'),
        image('assets/photos/33.jpg', 1760, 2200, '#1f2424'),
        image('assets/photos/man-under-snowy-mountain.jpg', 2200, 1458, '#8597a8'),
        video('assets/video/saskatchewan-2.mp4', 1920, 1080, '#3f391b'),
        image('assets/photos/21.jpg', 1760, 2200, '#718a92'),
        image('assets/photos/ellipsis-light.jpg', 1760, 2200, '#813107'),
        image('assets/photos/11.jpg', 2000, 1325, '#212d2d'),
        image('assets/photos/cinestill400d-030.jpg', 1760, 2200, '#77797e'),
        image('assets/photos/22.jpg', 2000, 1325, '#261c09'),
        image('assets/photos/cinestill400d-039.jpg', 2087, 2200, '#918d86'),
        video('assets/video/fire-lookout-2.mp4', 1920, 1080, '#3c2b28'),
        image('assets/photos/gold-029.jpg', 2200, 1470, '#799095'),
        image('assets/photos/05.jpg', 1760, 2200, '#341c08'),
        image('assets/photos/gold-030.jpg', 2200, 1470, '#616e74'),
        image('assets/photos/29.jpg', 2000, 1325, '#39362e'),
        image('assets/photos/portra-006.jpg', 1469, 2200, '#998374'),
        video('assets/video/icefields-2.mp4', 1920, 1080, '#4c4857'),
        image('assets/photos/gold-032.jpg', 2200, 1470, '#5b4935'),
        image('assets/photos/04.jpg', 2000, 1325, '#627e82'),
        image('assets/photos/portra-008.jpg', 2200, 1470, '#524231'),
        image('assets/photos/27.jpg', 1760, 2200, '#555e5a'),
        image('assets/photos/14.jpg', 2000, 1325, '#555148'),
        image('assets/photos/kodakpro-017.jpg', 1470, 2200, '#14130d'),
        video('assets/video/saskatchewan-1.mp4', 1920, 1080, '#6b6773'),
        image('assets/photos/gold-051.jpg', 1470, 2200, '#4f5846'),
        image('assets/photos/26.jpg', 2000, 1325, '#63584f'),
        image('assets/photos/15.jpg', 1760, 2200, '#3a3c39'),
        image('assets/photos/cinestill400d-037.jpg', 1470, 2200, '#80715e'),
        image('assets/photos/28.jpg', 2000, 1325, '#424741'),
        image('assets/photos/ellipsis-corner.jpg', 1458, 2200, '#787d79'),
        video('assets/video/icefields-1.mp4', 1920, 1080, '#484142'),
        image('assets/photos/18.jpg', 1760, 2200, '#675d44'),
        image('assets/photos/06.jpg', 2000, 1325, '#726f6c'),
        image('assets/photos/portra-026.jpg', 1760, 2200, '#33352e'),
    ];
})();
