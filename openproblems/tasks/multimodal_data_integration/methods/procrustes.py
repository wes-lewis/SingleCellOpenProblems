from sklearn.decomposition import TruncatedSVD
import scipy.spatial
from ....tools.normalize import log_cpm
from ....tools.decorators import method
from ....tools.utils import check_version


@method(
    method_name="Procrustes",
    paper_name="Generalized Procrustes analysis",
    paper_url="https://link.springer.com/content/pdf/10.1007/BF02291478.pdf",
    paper_year=1975,
    code_url="https://docs.scipy.org/doc/scipy/reference/generated/"
    "scipy.spatial.procrustes.html",
    code_version=check_version("scipy"),
)
def procrustes(adata, n_svd=100):
    n_svd = min([n_svd, min(adata.X.shape) - 1, min(adata.obsm["mode2"].shape) - 1])
    log_cpm(adata)
    log_cpm(adata, obsm="mode2", obs="mode2_obs", var="mode2_var")
    X_pca = TruncatedSVD(n_svd).fit_transform(adata.X)
    Y_pca = TruncatedSVD(n_svd).fit_transform(adata.obsm["mode2"])
    X_proc, Y_proc, _ = scipy.spatial.procrustes(X_pca, Y_pca)
    adata.obsm["aligned"] = X_proc
    adata.obsm["mode2_aligned"] = Y_proc
    return adata
