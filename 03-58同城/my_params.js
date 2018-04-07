/**
 * Created by Blast on 2018-4-5.
 */


function getGTID(b, a, c) {
                function d(a, b, c) {
                    a = ("" + a).length < b ? (Array(b + 1).join("0") + a).slice(-b) : "" + a;
                    return -1 == c ? a : a.substring(0, c) + "-" + a.substring(c)
                }
                var e = {
                    home: "1",
                    index: "2",
                    list: "3",
                    detail: "4",
                    post: "5",
                    special: "6"
                };
                b = e[b] ? parseInt(e[b]).toString(16) : 0;
                a = a.split(",");
                a = a[a.length - 1];
                a = parseInt(a) ? parseInt(a).toString(16) : 0;
                c = c.split(",");
                c = c[c.length - 1];
                c = parseInt(c) ? parseInt(c).toString(16) : 0;
                e = (13).toString(16);
                return "llpccccc-tttt-txxx-xxxx-xxxxxxxxxxxx".replace(/x/g, function(a) {
                    return (16 * Math.random() | 0).toString(16)
                }).replace(/ccccc/, d(a, 5, -1)).replace(/tttt-t/, d(c, 5, 4)).replace(/p/, d(b, 1, -1)).replace(/ll/, d(e, 2, -1))
            }

function getPGTID(_trackURL) {
        g = k._trackPagetype || "";
        g = _trackURL.pagetype || g  || "NA";
        w = _trackURL.cate || "";
        F = _trackURL.area || "";
        N = getGTID(g, w, F);
}

